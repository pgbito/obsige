"use client"

import { useState, useEffect } from "react"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Card, CardHeader, CardContent } from "@/components/ui/card"

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
      <CardHeader className="text-center text-xl font-semibold">configuración</CardHeader>
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
