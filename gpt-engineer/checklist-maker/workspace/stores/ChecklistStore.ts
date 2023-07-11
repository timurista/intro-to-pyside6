import { action, observable } from 'mobx'
import { Checklist } from '../models/Checklist'

export class ChecklistStore {
  @observable checklists: Checklist[] = []

  @action.bound
  async fetchChecklists() {
    // Fetch checklists from the backend
  }

  @action.bound
  async createChecklist(checklist: Checklist) {
    // Create a new checklist
  }

  @action.bound
  async updateChecklist(checklist: Checklist) {
    // Update an existing checklist
  }

  @action.bound
  async deleteChecklist(checklist: Checklist) {
    // Delete a checklist
  }
}
