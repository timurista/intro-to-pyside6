import { observer } from 'mobx-react'
import React, { useEffect } from 'react'
import { useStores } from '../hooks/useStores'
import ChecklistItem from './ChecklistItem'

const ChecklistList: React.FC = observer(() => {
  const { checklistStore } = useStores()

  useEffect(() => {
    checklistStore.fetchChecklists()
  }, [checklistStore])

  return (
    <div>
      {checklistStore.checklists.map(checklist => (
        <ChecklistItem key={checklist.id} checklist={checklist} />
      ))}
    </div>
  )
})

export default ChecklistList
