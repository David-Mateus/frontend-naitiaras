import { motion } from 'framer-motion'
import { Star, MessageCircle } from 'lucide-react'
import { PRODUCTS, buildWhatsAppLink } from '../data/content'

const heading = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0, transition: { duration: 0.6 } },
}

function ProductCard({ product }) {
  return (
    <a
      href={buildWhatsAppLink(
        `Olá! Tenho interesse no produto "${product.title}" da Nai Tiaras.`
      )}
      target="_blank"
      rel="noopener noreferrer"
      className="group shrink-0 w-[230px] sm:w-[260px] lg:w-[280px] mr-5 sm:mr-7 bg-white rounded-3xl overflow-hidden shadow-md hover:shadow-xl flex flex-col transition-all duration-300 hover:-translate-y-1"
    >
      <div className="relative w-full aspect-[4/5] overflow-hidden bg-blush-100">
        <img
          src={product.image}
          alt={product.title}
          loading="lazy"
          className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
        />
        <div className="absolute inset-0 bg-black/40 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-300">
          <span className="inline-flex items-center gap-2 rounded-full bg-[#25D366] text-white px-4 py-2 text-sm font-semibold shadow-lg scale-95 group-hover:scale-100 transition-transform duration-300">
            <MessageCircle size={16} />
            Comprar pelo WhatsApp
          </span>
        </div>
      </div>
      <div className="p-5 flex flex-col flex-1 text-left">
        <h3 className="font-display font-semibold text-lg text-[#8B1528] mb-1.5">
          {product.title}
        </h3>
        <p className="mt-1 text-sm text-[#333333] font-body flex-1">
          {product.description}
        </p>
        <span className="mt-4 inline-flex items-center gap-1.5 text-[#E4758E] text-xs font-semibold">
          <Star size={13} />
          Sob encomenda
        </span>
      </div>
    </a>
  )
}

export default function Products() {
  return (
    <section id="produtos" className="py-16 sm:py-24 px-4 sm:px-6 bg-white">
      <div className="max-w-6xl mx-auto">
        <motion.div
          variants={heading}
          initial="hidden"
          whileInView="show"
          viewport={{ once: true, amount: 0.3 }}
          className="text-center max-w-2xl mx-auto mb-12 sm:mb-16"
        >
          <span className="inline-flex items-center gap-2 text-[#E4758E] font-semibold text-sm uppercase tracking-widest mb-3">
            Vitrine
          </span>
          <h2 className="font-display font-semibold text-3xl sm:text-4xl text-[#8B1528]">
            Nossos produtos
          </h2>
          <p className="mt-4 text-[#333333] font-body text-base sm:text-lg">
            Clique em qualquer peça para conversar com a gente no WhatsApp e garantir a sua.
          </p>
        </motion.div>

        <div className="group/carousel relative overflow-hidden">
          <div className="pointer-events-none absolute inset-y-0 left-0 w-12 sm:w-24 z-10 bg-gradient-to-r from-white to-transparent" />
          <div className="pointer-events-none absolute inset-y-0 right-0 w-12 sm:w-24 z-10 bg-gradient-to-l from-white to-transparent" />

          <div className="flex w-max animate-marquee group-hover/carousel:[animation-play-state:paused] motion-reduce:animate-none">
            {PRODUCTS.map((product) => (
              <ProductCard key={`a-${product.id}`} product={product} />
            ))}
            {PRODUCTS.map((product) => (
              <ProductCard key={`b-${product.id}`} product={product} />
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}
