import { defineConfig } from 'vite'
import react, { reactCompilerPreset } from '@vitejs/plugin-react'
import babel from '@rolldown/plugin-babel'
import path from 'path'
import { assinarPromocao } from './src/crypto/signPromocao.js'

function assinaturaLojaPlugin() {
  return {
    name: 'assinatura-loja',
    configureServer(server) {
      server.middlewares.use('/api/assinar-promocao', (req, res, next) => {
        if (req.method !== 'POST') return next()
        let body = ''
        req.on('data', (c) => { body += c })
        req.on('end', () => {
          try {
            const campos = JSON.parse(body || '{}')
            const { canonico, assinatura } = assinarPromocao(campos)
            res.setHeader('Content-Type', 'application/json')
            res.end(JSON.stringify({ canonico, assinatura }))
          } catch (err) {
            res.statusCode = 500
            res.setHeader('Content-Type', 'application/json')
            res.end(JSON.stringify({ erro: String(err && err.message || err) }))
          }
        })
      })
    },
  }
}

export default defineConfig({
  root: './index',
  plugins: [
    react(),
    babel({ presets: [reactCompilerPreset()] }),
    assinaturaLojaPlugin()
  ],
  resolve: {
    alias: {
      src: path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 5000,
  },
})
