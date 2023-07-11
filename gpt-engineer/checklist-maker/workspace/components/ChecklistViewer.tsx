import React from 'react'
import { Checklist } from '../models/Checklist'

interface ChecklistViewerProps {
  checklist: Checklist
}

const ChecklistViewer: React.FC<ChecklistViewerProps> = ({ checklist }) => {
  return (
    <div>
      {/* Display checklist in a slideshow format here */}
    </div>
  )
}

export default ChecklistViewer
