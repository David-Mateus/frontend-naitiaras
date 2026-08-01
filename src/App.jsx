import Header from './components/Header'
import Hero from './components/Hero'
import About from './components/About'
import Products from './components/Products'
import Footer from './components/Footer'
import FloatingWhatsApp from './components/FloatingWhatsApp'

export default function App() {
  return (
    <div className="min-h-screen bg-blush-50 overflow-x-hidden">
      <Header />
      <main>
        <Hero />
        <About />
        <Products />
      </main>
      <Footer />
      <FloatingWhatsApp />
    </div>
  )
}
