import { useState, useRef } from "react"

export default function UploadZone({ onUpload }) {
  const [dragging, setDragging] = useState(false)
  const inputRef = useRef()

  function handleDrop(e) {
    e.preventDefault()
    setDragging(false)
    const file = e.dataTransfer.files[0]
    if (file && file.type === "application/pdf") onUpload(file)
  }

  function handleChange(e) {
    const file = e.target.files[0]
    if (file) onUpload(file)
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] space-y-8">
      <div className="text-center space-y-3">
        <h2 className="text-3xl font-bold">Upload your contract</h2>
        <p className="text-gray-400 max-w-md">
          We'll scan it for risky clauses, one-sided terms, and red flags — and explain them in plain English.
        </p>
      </div>

      <div
        onDragOver={(e) => { e.preventDefault(); setDragging(true) }}
        onDragLeave={() => setDragging(false)}
        onDrop={handleDrop}
        onClick={() => inputRef.current.click()}
        className={`w-full max-w-lg border-2 border-dashed rounded-2xl p-16 text-center cursor-pointer transition-all
          ${dragging ? "border-blue-500 bg-blue-500/10" : "border-gray-700 hover:border-gray-500 hover:bg-gray-900"}`}
      >
        <div className="text-5xl mb-4">📄</div>
        <p className="text-gray-300 font-medium">Drop your PDF here</p>
        <p className="text-gray-500 text-sm mt-1">or click to browse</p>
        <input
          ref={inputRef}
          type="file"
          accept=".pdf"
          className="hidden"
          onChange={handleChange}
        />
      </div>

      <p className="text-xs text-gray-600">PDF files only · Max 10MB · Processed securely</p>
    </div>
  )
}
