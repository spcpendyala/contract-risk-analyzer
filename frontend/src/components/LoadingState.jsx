export default function LoadingState() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] space-y-6">
      <div className="w-12 h-12 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" />
      <div className="text-center space-y-2">
        <p className="text-gray-300 font-medium">Analyzing your contract...</p>
        <p className="text-gray-500 text-sm">This usually takes 10–20 seconds</p>
      </div>
    </div>
  )
}
