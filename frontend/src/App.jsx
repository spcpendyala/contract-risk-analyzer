import { useState } from "react"
import UploadZone from "./components/UploadZone"
import RiskReport from "./components/RiskReport"
import LoadingState from "./components/LoadingState"
import axios from "axios"

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000"

export default function App() {
  const [status, setStatus] = useState("idle") // idle | loading | done | error
  const [report, setReport] = useState(null)
  const [error, setError] = useState(null)

  async function handleUpload(file) {
    setStatus("loading")
    setError(null)
    const formData = new FormData()
    formData.append("file", file)
    try {
      const res = await axios.post(`${API_URL}/analyze`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      })
      setReport(res.data)
      setStatus("done")
    } catch (err) {
      setError(err.response?.data?.detail || "Something went wrong. Please try again.")
      setStatus("error")
    }
  }

  function handleReset() {
    setStatus("idle")
    setReport(null)
    setError(null)
  }

  return (
    <div className="min-h-screen bg-gray-950 text-white">
      <header className="border-b border-gray-800 px-6 py-4">
        <div className="max-w-4xl mx-auto flex items-center justify-between">
          <div>
            <h1 className="text-xl font-semibold tracking-tight">Contract Risk Analyzer</h1>
            <p className="text-sm text-gray-400">AI-powered contract review in seconds</p>
          </div>
          {status === "done" && (
            <button
              onClick={handleReset}
              className="text-sm text-gray-400 hover:text-white transition-colors"
            >
              ← Analyze another
            </button>
          )}
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-6 py-12">
        {status === "idle" && <UploadZone onUpload={handleUpload} />}
        {status === "loading" && <LoadingState />}
        {status === "error" && (
          <div className="text-center space-y-4">
            <p className="text-red-400">{error}</p>
            <button onClick={handleReset} className="text-sm text-gray-400 hover:text-white">
              Try again
            </button>
          </div>
        )}
        {status === "done" && report && <RiskReport report={report} />}
      </main>
    </div>
  )
}
