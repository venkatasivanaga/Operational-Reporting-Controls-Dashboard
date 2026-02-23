import { useEffect, useState } from 'react'
import { getMetricsSummary, type MetricsSummary } from './lib/api'

function pct(v: number | null): string {
  if (v === null) return '--'
  return String(Math.round(v * 100)) + '%'
}

function hrs(v: number | null): string {
  if (v === null) return '--'
  return v.toFixed(1)
}

export default function App() {
  const [m, setM] = useState<MetricsSummary | null>(null)
  const [err, setErr] = useState<string | null>(null)

  useEffect(() => {
    getMetricsSummary()
      .then((d) => {
        setM(d)
        setErr(null)
      })
      .catch((e: unknown) => {
        setErr(e instanceof Error ? e.message : 'Failed to load metrics')
      })
  }, [])

  return (
    <div className='min-h-screen bg-white text-zinc-900'>
      <header className='border-b border-zinc-200'>
        <div className='mx-auto max-w-6xl px-4 py-4 flex items-center justify-between'>
          <div className='font-semibold tracking-tight'>Operational Reporting Controls</div>
          <div className='text-sm text-zinc-600'>Live metrics</div>
        </div>
      </header>

      <main className='mx-auto max-w-6xl px-4 py-8'>
        <h1 className='text-xl font-semibold'>Dashboard</h1>

        {err && (
          <div className='mt-4 rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700'>
            {err}
          </div>
        )}

        <div className='mt-6 grid grid-cols-1 gap-4 sm:grid-cols-3'>
          <div className='rounded-xl border border-zinc-200 p-5 shadow-sm'>
            <div className='text-sm text-zinc-600'>Open incidents</div>
            <div className='mt-2 text-2xl font-semibold'>{m ? m.open_incidents : '...'}</div>
          </div>

          <div className='rounded-xl border border-zinc-200 p-5 shadow-sm'>
            <div className='text-sm text-zinc-600'>Pass rate</div>
            <div className='mt-2 text-2xl font-semibold'>{m ? pct(m.pass_rate) : '...'}</div>
          </div>

          <div className='rounded-xl border border-zinc-200 p-5 shadow-sm'>
            <div className='text-sm text-zinc-600'>MTTR (hrs)</div>
            <div className='mt-2 text-2xl font-semibold'>{m ? hrs(m.mttr_hours) : '...'}</div>
          </div>
        </div>
      </main>
    </div>
  )
}
