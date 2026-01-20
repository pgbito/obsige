"use client"

import { useState } from "react"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Card, CardHeader, CardContent } from "@/components/ui/card"
const API_URL = "40.233.20.225:8000"
export default function Home() {
  const [user, setUser] = useState("")
  const [data, setData] = useState<any>(null)
  const [loading, setLoading] = useState(false)

  const fetchInfo = async () => {
    setLoading(true)
    setData(null)
    try {
      const sessId = localStorage.getItem("sessId") || ""
      const res = await fetch(`http://${API_URL}/consulta?user=${user}&sessId=${sessId}`)
      const json = await res.json()
      setData(json)
    } catch (err) {
      console.error(err)
      alert("error al obtener datos")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex flex-col items-center gap-6">
      <Card className="w-[360px] shadow-lg rounded-2xl p-6">
        <CardHeader className="text-center text-xl font-semibold">consulta de usuario</CardHeader>
        <CardContent className="flex flex-col gap-4">
          <Input
            placeholder="@usuario"
            value={user}
            onChange={(e) => setUser(e.target.value)}
          />
          <Button onClick={fetchInfo} disabled={loading || !user}>
            {loading ? "buscando..." : "buscar"}
          </Button>
        </CardContent>
      </Card>

      {data && (
        <div className="w-[360px] flex flex-col gap-6">
          <Section title="No Mutuals (rogados😴)" items={data.nomutuals} />
          <Section title="Mutuals" items={data.mutuals} />
          
        </div>
      )}
    </div>
  )
}

function Section({ title, items }: { title: string; items: Record<string, any> }) {
  const entries = Object.values(items || {})
  if (!entries.length) return null
  return (
    <Card className="p-4 rounded-2xl shadow-md">
      <h3 className="font-semibold text-lg mb-3">{title}</h3>
      <div className="flex flex-col gap-3">
        {entries.map((u: any) => (
          <div key={u.id} className="flex items-center gap-3 p-2 hover:bg-gray-50 rounded-xl">
            <img
              src={`http://${API_URL}/imagen?uid=${u.id}`}
              alt={u.username}
              className="w-10 h-10 rounded-full"
            />
            <div>
              <p className="font-medium">{u.username}</p>
            </div>
          </div>
        ))}
      </div>
    </Card>
  )
}
