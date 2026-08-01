import { motion } from 'framer-motion'
import { Heart } from 'lucide-react'
import { COMPANY } from '../data/content'

export default function About() {
  const [paragraph1, paragraph2] = COMPANY.history.split('\n\n')
  const [beforeDate, afterDate] = paragraph1.split(COMPANY.foundedLabel)

  return (
    <section id="sobre" className="py-24 px-4 sm:px-6 bg-[#FDF2F4]">
      <div className="max-w-6xl mx-auto grid md:grid-cols-2 gap-12 md:gap-16 items-center">
        <motion.div
          initial={{ opacity: 0, x: -30 }}
          whileInView={{ opacity: 1, x: 0 }}
          viewport={{ once: true, amount: 0.3 }}
          transition={{ duration: 0.7 }}
          className="order-2 md:order-1"
        >
          <span className="inline-flex items-center gap-2 text-[#E4758E] font-semibold text-sm uppercase tracking-wide mb-3">
            Sobre nós
          </span>

          <h2 className="font-display font-semibold text-3xl sm:text-4xl text-[#8B1528] mb-5">
            Uma história feita de laços
          </h2>

          <div className="space-y-4 text-[#333333] font-body leading-relaxed text-base sm:text-lg">
            <p>
              {beforeDate}
              <strong className="font-semibold">{COMPANY.foundedLabel}</strong>
              {afterDate}
            </p>
            <p>{paragraph2}</p>
          </div>

          <div className="mt-7 grid grid-cols-3 gap-3 sm:gap-4">
            {COMPANY.stats.map((stat) => (
              <div
                key={stat.label}
                className="rounded-2xl bg-white px-3 py-4 text-center shadow-sm"
              >
                <p className="font-display font-semibold text-lg sm:text-xl text-[#8B1528]">
                  {stat.value}
                </p>
                <p className="text-xs text-gray-600 mt-0.5">{stat.label}</p>
              </div>
            ))}
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, x: 30 }}
          whileInView={{ opacity: 1, x: 0 }}
          viewport={{ once: true, amount: 0.3 }}
          transition={{ duration: 0.7 }}
          className="order-1 md:order-2"
        >
          <div className="relative">
            <div className="bg-white p-3 sm:p-4 rounded-3xl shadow-soft">
              <div className="aspect-[4/5] rounded-2xl overflow-hidden">
                <img
                  src="/assets/produto-4.jpeg"
                  alt={`Sobre a ${COMPANY.name}`}
                  className="w-full h-full object-cover"
                />
              </div>
            </div>

            <span className="absolute -bottom-4 left-4 sm:left-6 inline-flex items-center gap-2 rounded-full bg-[#8B1528] text-white text-xs sm:text-sm font-semibold px-4 py-2 shadow-soft">
              <Heart size={14} className="text-white" />
              Feito à mão
            </span>
          </div>
        </motion.div>
      </div>
    </section>
  )
}
