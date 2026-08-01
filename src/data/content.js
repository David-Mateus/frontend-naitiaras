// Configuração central da Nai Tiaras.
// Edite os textos e o número de WhatsApp aqui — o resto do site consome deste arquivo.

export const COMPANY = {
  name: 'Nai Tiaras',
  slogan: 'Tudo para sua princesa',
  foundedLabel: '15 de janeiro de 2015',
  foundedISO: '2015-01-15',
  // Texto de exemplo — substitua pela história real da empresa quando desejar.
  history: `A Nai Tiaras nasceu em 15 de janeiro de 2015, de um sonho simples: transformar fitas, rendas e muito amor em acessórios que fazem meninas e bebês se sentirem especiais. O que começou dentro de casa, peça por peça, virou referência em tiaras e laços artesanais.

Cada produto é montado à mão, com atenção ao acabamento e ao conforto. Mais de uma década depois, seguimos com o mesmo cuidado do primeiro laço — e com a confiança de centenas de famílias que voltam sempre.`,
  stats: [
    { value: '2015', label: 'Fundação' },
    { value: '100%', label: 'Artesanal' },
    { value: '+10 anos', label: 'De carinho' },
  ],
}

export const WHATSAPP = {
  displayNumber: '+55 81 8586-4521',
  // Apenas dígitos, com código do país — usado no link wa.me
  digits: '558185864521',
  defaultMessage:
    'Olá! Vim pelo site da Nai Tiaras e gostaria de saber mais sobre os produtos.',
}

export function buildWhatsAppLink(message = WHATSAPP.defaultMessage) {
  return `https://wa.me/${WHATSAPP.digits}?text=${encodeURIComponent(message)}`
}

export const PRODUCTS = [
  {
    id: 1,
    title: 'Faixas Crochê Coloridas',
    description: 'Kit com laços em crochê e meia de seda',
    image: '/assets/produto-1.jpeg',
  },
  {
    id: 2,
    title: 'Laços Gorgurão Sunset',
    description: 'Trio de laços em degradê laranja e amarelo',
    image: '/assets/produto-2.jpeg',
  },
  {
    id: 3,
    title: 'Laços Candy Color',
    description: 'Trio vibrante azul, tie-dye e pink',
    image: '/assets/produto-3.jpeg',
  },
  {
    id: 4,
    title: 'Faixa Pérola & Corações',
    description: 'Delicadeza em tons pastéis com aplique',
    image: '/assets/produto-4.jpeg',
  },
  {
    id: 5,
    title: 'Laço Duplo Renda Branca',
    description: 'Par de laços delicados em renda para ocasiões especiais',
    image: '/assets/produto-5.jpeg',
  },
  {
    id: 6,
    title: 'Tiara Flor Bordada',
    description: 'Tiara artesanal com flor bordada à mão',
    image: '/assets/produto-6.jpeg',
  },
]
