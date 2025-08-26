export interface Club {
  id: number
  bookTitle: string
  bookAuthors: string
  publicationYear: number
  description: string
  telegramChatLink: string
  owner: number
  members: number[]
}

export interface PaginatedClubList {
  count: number
  next: string | null
  previous: string | null
  results: Club[]
}
