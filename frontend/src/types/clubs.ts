import type { User } from './users'

export interface Club {
  id: number
  bookTitle: string
  bookAuthors: string
  publicationYear: number
  description: string
  telegramChatLink: string
  owner: User
  members: number[]
}

export interface PaginatedClubList {
  count: number
  next: string | null
  previous: string | null
  results: Club[]
}

export interface BookReview {
  id: number
  club: number
  user: User
  username?: string
  review: string
  assessment: number
  readPages: number
  createdAt?: string
}

export interface PaginatedBookReviewList {
  count: number
  next: string | null
  previous: string | null
  results: BookReview[]
}
