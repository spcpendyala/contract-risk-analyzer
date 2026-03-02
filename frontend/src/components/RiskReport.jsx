import RiskCard from "./RiskCard"

const riskColors = {
  LOW: "text-blue-400",
  MEDIUM: "text-yellow-400",
  HIGH: "text-red-400",
  CRITICAL: "text-red-500",
}

export default function RiskReport({ report }) {
  const high = report.findings.filter(f => f.severity === "high").length
  const medium = report.findings.filter(f => f.severity === "medium").length
  const low = report.findings.filter(f => f.severity === "low").length

  return (
    <div className="space-y-8">
      {/* Summary */}
      <div className="bg-gray-900 rounded-2xl p-6 space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-bold">Analysis Complete</h2>
          <span className={`text-2xl font-bold ${riskColors[report.overall_risk] || "text-white"}`}>
            {report.overall_risk} RISK
          </span>
        </div>
        <p className="text-gray-300">{report.summary}</p>
        <div className="flex gap-4 pt-2">
          <div className="text-center">
            <div className="text-2xl font-bold text-red-400">{high}</div>
            <div className="text-xs text-gray-500">High</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-yellow-400">{medium}</div>
            <div className="text-xs text-gray-500">Medium</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-blue-400">{low}</div>
            <div className="text-xs text-gray-500">Low</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-white">{report.findings.length}</div>
            <div className="text-xs text-gray-500">Total</div>
          </div>
        </div>
      </div>

      {/* Findings */}
      <div className="space-y-4">
        <h3 className="font-semibold text-gray-300">Findings</h3>
        {report.findings.length === 0 ? (
          <p className="text-gray-500 text-center py-8">No significant risks found.</p>
        ) : (
          report.findings
            .sort((a, b) => {
              const order = { high: 0, medium: 1, low: 2 }
              return (order[a.severity] ?? 3) - (order[b.severity] ?? 3)
            })
            .map((finding, i) => <RiskCard key={i} finding={finding} />)
        )}
      </div>
    </div>
  )
}
