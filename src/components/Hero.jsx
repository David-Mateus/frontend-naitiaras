import { motion } from 'framer-motion'
import { MessageCircle, Sparkles, ArrowRight } from 'lucide-react'
import { COMPANY, buildWhatsAppLink } from '../data/content'

function scrollToId(id) {
  const el = document.getElementById(id)
  if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

export default function Hero() {
  return (
    <section
      id="inicio"
      className="relative pt-32 sm:pt-44 pb-24 sm:pb-36 px-4 sm:px-6 bg-white"
    >
      <div className="relative max-w-5xl mx-auto text-center flex flex-col items-center">
        <motion.span
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="inline-flex items-center gap-2 rounded-full bg-[#FDF2F4] border border-[#f6c9db] px-4 py-1.5 text-xs sm:text-sm font-semibold uppercase tracking-wider text-[#333333] mb-6"
        >
          <Sparkles size={14} className="text-gold-500" />
          Artesanal desde 2015
        </motion.span>

        <motion.h1
          initial={{ opacity: 0, y: 24 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.1 }}
          className="font-display font-normal text-4xl xs:text-5xl sm:text-6xl md:text-7xl leading-[1.1] text-[#8B1528]"
        >
          {COMPANY.slogan}
        </motion.h1>

        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.25 }}
          className="mt-6 max-w-xl text-base sm:text-lg text-[#333333] font-body"
        >
          Tiaras, laços e faixas feitos à mão com carinho, capricho e materiais
          selecionados — para deixar cada detalhe ainda mais encantador.
        </motion.p>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.4 }}
          className="mt-9 flex flex-row flex-wrap items-center justify-center gap-4"
        >
          <button
            onClick={() => scrollToId('produtos')}
            className="w-fit inline-flex items-center justify-center gap-2 rounded-full bg-[#8B1528] hover:bg-[#711120] text-white font-semibold px-8 py-3 text-base shadow-soft transition-transform hover:scale-[1.03] active:scale-95"
          >
            Ver Produtos
            <ArrowRight size={18} />
          </button>

          <a
            href={buildWhatsAppLink()}
            target="_blank"
            rel="noopener noreferrer"
            className="w-fit inline-flex items-center justify-center gap-2 rounded-full bg-[#25D366] hover:bg-[#1ebe5b] text-white font-semibold px-8 py-3 text-base shadow-soft transition-transform hover:scale-[1.03] active:scale-95"
          >
            <MessageCircle size={18} />
            Contato Rápido
          </a>
        </motion.div>
      </div>
    </section>
  )
}
