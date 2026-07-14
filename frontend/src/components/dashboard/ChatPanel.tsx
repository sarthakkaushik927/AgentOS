import { useState, useRef, useEffect } from 'react'
import type { FormEvent } from 'react'
import { Card } from '../common/Card'
import { Button } from '../common/Button'
import { Send } from 'lucide-react'
import { API_BASE_URL } from '../../env'


interface Message {
  id: string
  role: 'user' | 'agent'
  content: string
}

export function ChatPanel() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [isTyping, setIsTyping] = useState(false)
  const bottomRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, isTyping])

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    if (!input.trim()) return

    const userMessage: Message = { id: Date.now().toString(), role: 'user', content: input }
    setMessages(prev => [...prev, userMessage])
    setInput('')
    setIsTyping(true)

    try {
      const token = localStorage.getItem('access_token')
      const response = await fetch(`${API_BASE_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ message: input })
      })

      if (!response.ok) throw new Error('Network response was not ok')
      
      const reader = response.body?.getReader()
      const decoder = new TextDecoder()
      
      const agentMessage: Message = { id: (Date.now() + 1).toString(), role: 'agent', content: '' }
      setMessages(prev => [...prev, agentMessage])

      if (reader) {
        while (true) {
          const { done, value } = await reader.read()
          if (done) break
          const chunk = decoder.decode(value, { stream: true })
          // In a real SSE, we parse event types. Here we just append raw data for the stub.
          setMessages(prev => {
            const updated = [...prev]
            updated[updated.length - 1].content += chunk
            return updated
          })
        }
      }
    } catch (error) {
      setMessages(prev => [
        ...prev, 
        { id: Date.now().toString(), role: 'agent', content: 'Connection failed or agent stub returned 500 error.' }
      ])
    } finally {
      setIsTyping(false)
    }
  }

  return (
    <Card title="Terminal" className="h-full flex flex-col">
      <div className="flex-1 overflow-y-auto space-y-4 mb-4">
        {messages.length === 0 && (
          <div className="text-slate text-sm font-mono text-center mt-10">
            Awaiting command...
          </div>
        )}
        {messages.map((m) => (
          <div key={m.id} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[80%] rounded-base p-3 text-sm ${m.role === 'user' ? 'bg-surface border border-hairline' : 'bg-transparent border-l-2 border-signal font-mono'}`}>
              {m.content}
            </div>
          </div>
        ))}
        {isTyping && (
          <div className="flex justify-start">
            <div className="bg-transparent border-l-2 border-signal p-3 text-signal animate-pulse font-mono text-xs">
              Agent processing...
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>
      <form onSubmit={handleSubmit} className="flex gap-2 shrink-0">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Execute task..."
          className="flex-1 px-4 py-2 bg-surface border border-hairline rounded-base text-ink focus:outline-none focus:border-signal font-mono text-sm"
          disabled={isTyping}
        />
        <Button type="submit" disabled={isTyping || !input.trim()}>
          <Send size={16} />
        </Button>
      </form>
    </Card>
  )
}
