const severityConfig = {
  high: { bg: "bg-red-500/10", border: "border-red-500/30", badge: "bg-red-500/20 text-red-400", dot: "bg-red-500" },
  medium: { bg: "bg-yellow-500/10", border: "border-yellow-500/30", badge: "bg-yellow-500/20 text-yellow-400", dot: "bg-yellow-500" },
  low: { bg: "bg-blue-500/10", border: "border-blue-500/30", badge: "bg-blue-500/20 text-blue-400", dot: "bg-blue-400" },
}

export default function RiskCard({ finding }) {
  const config = severityConfig[finding.severity] || severityConfig.low

  return (
    <div className={`rounded-xl border p-5 space-y-3 ${config.bg} ${config.border}`}>
      <div className="flex items-start justify-between gap-3">
        <div className="flex items-center gap-2">
          <div className={`w-2 h-2 rounded-full mt-1 flex-shrink-0 ${config.dot}`} />
          <h3 className="font-semibold text-white">{finding.title}</h3>
        </div>
        <div className="flex gap-2 flex-shrink-0">
          <span className={`text-xs px-2 py-1 rounded-full font-medium ${config.badge}`}>
            {finding.severity.toUpperCase()}
          </span>
          <span className="text-xs px-2 py-1 rounded-full bg-gray-700/50 text-gray-400">
            {finding.category}
          </span>
        </div>
      </div>
      <p className="text-gray-300 text-sm leading-relaxed">{finding.explanation}</p>
      {finding.suggestion && (
        <div className="bg-gray-900/50 rounded-lg p-3">
          <p className="text-xs text-gray-500 font-medium mb-1">SUGGESTION</p>
          <p className="text-gray-400 text-sm">{finding.suggestion}</p>
        </div>
      )}
    </div>
  )
}
