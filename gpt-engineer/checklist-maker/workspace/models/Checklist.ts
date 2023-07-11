export class Checklist {
  id: string
  title: string
  questions: { question: string, description: string, answer: string }[]

  constructor(id: string, title: string, questions: { question: string, description: string, answer: string }[]) {
    this.id = id
    this.title = title
    this.questions = questions
  }
}
