export default function App() {
  return (
    <div className='min-h-screen bg-white text-zinc-900'>
      <header className='border-b border-zinc-200'>
        <div className='mx-auto max-w-6xl px-4 py-4 flex items-center justify-between'>
          <div className='font-semibold tracking-tight'>Operational Reporting Controls</div>
          <div className='text-sm text-zinc-600'>Frontend scaffold</div>
        </div>
      </header>

      <main className='mx-auto max-w-6xl px-4 py-8'>
        <div className='rounded-xl border border-zinc-200 p-6 shadow-sm'>
          <h1 className='text-xl font-semibold'>Dashboard</h1>
          <p className='mt-2 text-zinc-600'>
            Next: connect to backend metrics and show KPI cards.
          </p>
        </div>
      </main>
    </div>
  )
}
