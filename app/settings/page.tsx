"use client"

import { useState, useEffect } from "react"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Card, CardHeader, CardContent, CardAction, CardTitle } from "@/components/ui/card"
import Link from "next/link"
export default function Settings() {
  const [sessId, setSessId] = useState("")
  
  useEffect(() => {
    const saved = localStorage.getItem("sessId")
    if (saved) setSessId(saved)
  }, [])

  const saveSessId = () => {
    localStorage.setItem("sessId", sessId)
    alert("sessId guardado correctamente 🔒")
  }

  return (
    <Card className="w-[360px] shadow-lg rounded-2xl p-6">
      <CardHeader className="text-center text-xl font-bold">⚙️ configuración </CardHeader>
      <CardTitle className="text-center text-xl font-semibold">Colocar sessId (credenciales) </CardTitle>
       
       <Link
    href="https://github.com/pgbito/obsige#credenciales"
    target="_blank"
    className="text-center text-blue-500 font-bold"
  >¿cómo consigo esa vara?</Link>
      <CardContent className="flex flex-col gap-4">
        <Input
          placeholder="sessId"
          value={sessId}
          onChange={(e) => setSessId(e.target.value)}
        />
        <Button onClick={saveSessId}>guardar</Button>
      </CardContent>
    </Card>
  )
}
