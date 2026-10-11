import { useEffect, useState } from 'react'

export default function App() {
  const [message, setMessage] = useState('Conectando...')

  useEffect(() => {
    fetch(`${import.meta.env.VITE_API_URL}/health`)
      .then((response) => {
        if (!response.ok) throw new Error('Error del servidor')
        return response.json()
      })
      .then((data: { status: string }) => setMessage(data.status))
      .catch(() => setMessage('No se pudo conectar con el backend'))
  }, [])

  return <main>Estado del backend: {message}</main>
}