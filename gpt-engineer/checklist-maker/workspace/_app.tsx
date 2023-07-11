import { Provider } from 'mobx-react'
import { AppProps } from 'next/app'
import React from 'react'
import '../styles/globals.css'
import { ChecklistStore } from '../stores/ChecklistStore'

function MyApp({ Component, pageProps }: AppProps) {
  const checklistStore = new ChecklistStore()

  return (
    <Provider checklistStore={checklistStore}>
      <Component {...pageProps} />
    </Provider>
  )
}

export default MyApp
