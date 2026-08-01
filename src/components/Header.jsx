import { motion } from 'framer-motion'
import { MessageSquare } from 'lucide-react'
import { COMPANY, buildWhatsAppLink } from '../data/content'

function scrollToId(id) {
  const el = document.getElementById(id)
  if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

export default function Header() {
  return (
    <motion.header
      initial={{ y: -80, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.6, ease: 'easeOut' }}
      className="fixed top-0 left-0 right-0 z-50 bg-white border-b border-gray-100 shadow-sm"
    >
      <div className="max-w-6xl mx-auto px-4 sm:px-6 h-16 sm:h-20 flex items-center justify-between">
        <button
          onClick={() => scrollToId('inicio')}
          className="flex items-center gap-2 sm:gap-3 shrink-0"
          aria-label={`${COMPANY.name} - início`}
        >
          <img
            src="/assets/logo.png"
            alt={COMPANY.name}
            className="h-9 sm:h-12 w-auto object-contain"
          />
          <span className="font-display font-semibold text-lg sm:text-xl text-rose-500">
            {COMPANY.name}
          </span>
        </button>

        <a
          href={buildWhatsAppLink()}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center gap-2 rounded-full bg-[#25D366] hover:bg-[#1ebe5b] text-white font-semibold px-3.5 py-2 sm:px-5 sm:py-2.5 text-sm sm:text-base shadow-soft transition-transform active:scale-95 hover:scale-[1.03]"
        >
          <MessageSquare size={18} className="shrink-0" />
          <span className="hidden xs:inline sm:inline">Fale Conosco</span>
        </a>
      </div>
    </motion.header>
  )
}
