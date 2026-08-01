import { Instagram, Phone } from 'lucide-react'
import { COMPANY, WHATSAPP, buildWhatsAppLink } from '../data/content'

export default function Footer() {
  const year = new Date().getFullYear()

  return (
    <footer id="contato" className="bg-burgundy-700 text-blush-50">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 py-14 sm:py-16 grid grid-cols-1 md:grid-cols-3 gap-12">
        <div>
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-white shadow-sm p-2 mb-4">
            <img
              src="/assets/logo.png"
              alt={COMPANY.name}
              className="h-full w-full object-contain"
            />
          </div>
          <p className="text-white/80 text-sm leading-relaxed">
            {COMPANY.slogan}. Acessórios exclusivos feitos com carinho para encantar a sua
            pequena.
          </p>
        </div>

        <div>
          <h3 className="font-display font-semibold text-lg text-white mb-6">Contato</h3>
          <a
            href={buildWhatsAppLink()}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-2 text-white/80 hover:text-pink-300 transition-colors text-sm"
          >
            <Phone size={16} />
            {WHATSAPP.displayNumber}
          </a>
        </div>

        <div>
          <h3 className="font-display font-semibold text-lg text-white mb-6">Redes sociais</h3>
          <a
            href="#"
            className="inline-flex items-center gap-2 text-white/80 hover:text-pink-300 transition-colors text-sm"
          >
            <Instagram size={16} />
            @naitiaras
          </a>
        </div>
      </div>

      <div className="border-t border-white/10 py-5 px-4 text-center text-xs text-blush-100/60">
        © {year} {COMPANY.name}. Todos os direitos reservados.
      </div>
    </footer>
  )
}
