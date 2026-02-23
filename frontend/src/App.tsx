import { useEffect, useMemo, useState } from 'react'
import { getMetricsSummary, type MetricsSummary } from './lib/api'

function formatPercent(value: number | null) {
  if (value === null) return '—'
  return ${Math.round(value * 100)}%
}

function formatNumber(value: number | null) {
  if (value === null) return '—'
  return value.toFixed(1)
}

export default function App() {
  const [data, setData] = useState<MetricsSummary | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let alive = true
    setLoading(true)
    getMetricsSummary()
      .then((d) => {
        if (!alive) return
        setData(d)
        setError(null)
      })
      .catch((e: unknown) => {
        if (!alive) return
        setError(e instanceof Error ? e.message : 'Failed to load metrics')
      })
      .finally(() => {
        if (!alive) return
        setLoading(false)
      })

    return () => {
      alive = false
    }
  }, [])

  const cards = useMemo(() => {
    return [
      { label: 'Open incidents', value: data?.open_incidents ?? null, format: (v: number | null) => (v ?? '—') },
      { label: 'Pass rate', value: data?.pass_rate ?? null, format: formatPercent },
      { label: 'MTTR (hrs)', value: data?.mttr_hours ?? null, format: formatNumber },
    ]
  }, [data])

  return (
    <div className='min-h-screen bg-white text-zinc-900'>
      <header className='border-b border-zinc-200'>
        <div className='mx-auto max-w-6xl px-4 py-4 flex items-center justify-between'>
          <div className='font-semibold tracking-tight'>Operational Reporting Controls</div>
          <div className='text-sm text-zinc-600'>Live metrics</div>
        </div>
      </header>

      <main className='mx-auto max-w-6xl px-4 py-8'>
        <div className='flex items-start justify-between gap-4'>
          <div>
            <h1 className='text-xl font-semibold'>Dashboard</h1>
            <p className='mt-1 text-sm text-zinc-600'>
              Pulling KPIs from <span className='font-mono'>/api/metrics/summary</span>
            </p>
          </div>

          <a
            className='text-sm underline text-zinc-700 hover:text-zinc-900'
            href='http://127.0.0.1:8000/docs'
            target='_blank'
            rel='noreferrer'
          >
            API docs
          </a>
        </div>

        <div className='mt-6 grid grid-cols-1 gap-4 sm:grid-cols-3'>
          {cards.map((c) => (
            <div key={c.label} className='rounded-xl border border-zinc-200 p-5 shadow-sm'>
              <div className='text-sm text-zinc-600'>{c.label}</div>
              <div className='mt-2 text-2xl font-semibold'>
                {loading ? '…' : c.format(c.value as number | null)}
              </div>
            </div>
          ))}
        </div>

        {error && (
          <div className='mt-6 rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700'>
            {error}
            <div className='mt-2 text-xs text-red-700/80'>
              Make sure the backend is running at <span className='font-mono'>http://127.0.0.1:8000</span>.
            </div>
          </div>
        )}

        {data && (
          <div className='mt-6 grid grid-cols-1 gap-4 md:grid-cols-2'>
            <div className='rounded-xl border border-zinc-200 p-5'>
              <div className='text-sm font-medium'>Incidents by status</div>
              <pre className='mt-2 text-xs text-zinc-700 overflow-auto'>
                {JSON.stringify(data.incidents_by_status, null, 2)}
              </pre>
            </div>
            <div className='rounded-xl border border-zinc-200 p-5'>
              <div className='text-sm font-medium'>Tests by result</div>
              <pre className='mt-2 text-xs text-zinc-700 overflow-auto'>
                {JSON.stringify(data.tests_by_result, null, 2)}
              </pre>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}
