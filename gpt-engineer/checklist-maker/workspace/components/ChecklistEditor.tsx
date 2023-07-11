import React from 'react'
import { Checklist } from '../models/Checklist'

interface ChecklistEditorProps {
  checklist: Checklist
}

const ChecklistEditor: React.FC<ChecklistEditorProps> = ({ checklist }) => {
  return (
    <div>
      {/* Checklist editing form goes here */}
    </div>
  )
}

export default ChecklistEditor
