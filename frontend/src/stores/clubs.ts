import { defineStore } from 'pinia'
import axios from 'axios'
import type { Club, PaginatedClubList } from '@/types/clubs'

interface ClubsState {
  clubs: Club[]
  isLoading: boolean
  error: string | null
  pagination: {
    count: number
    next: string | null
    previous: string | null
    currentPage: number
    pageSize: number
  }
}

export const useClubsStore = defineStore('clubs', {
  state: (): ClubsState => ({
    clubs: [],
    isLoading: false,
    error: null,
    pagination: {
      count: 0,
      next: null,
      previous: null,
      currentPage: 1,
      pageSize: 10,
    },
  }),

  actions: {
    async _fetchClubsWithParams(
      params: Record<string, string | number>,
      errorMessage: string,
    ) {
      this.isLoading = true
      this.error = null
      try {
        const searchParams = new URLSearchParams(
          Object.entries(params).map(([k, v]) => [k, String(v)]),
        )
        const response = await axios.get<PaginatedClubList>(
          `/api/v1/clubs/?${searchParams.toString()}`,
        )
        this.clubs = response.data.results
        this.pagination = {
          count: response.data.count,
          next: response.data.next,
          previous: response.data.previous,
          currentPage: (params.page as number) ?? 1,
          pageSize: (params.page_size as number) ?? 10,
        }
      } catch (error) {
        this.error = errorMessage
        console.error('Error fetching clubs:', error)
      } finally {
        this.isLoading = false
      }
    },

    async fetchClubs(page: number = 1, pageSize: number = 10) {
      await this._fetchClubsWithParams(
        { page, page_size: pageSize },
        'Не удалось загрузить список клубов',
      )
    },

    async searchClubs(query: string, page: number = 1, pageSize: number = 10) {
      await this._fetchClubsWithParams(
        { search: query, page, page_size: pageSize },
        'Ошибка при поиске клубов',
      )
    },

    async filterByMembership(
      type: 'member' | 'owner' | 'all',
      page: number = 1,
      pageSize: number = 10,
    ) {
      const params: Record<string, string | number> = { page, page_size: pageSize }
      if (type !== 'all') params.membership = type
      await this._fetchClubsWithParams(
        params,
        'Ошибка при фильтрации клубов',
      )
    },

    async nextPage() {
      if (this.pagination.next) {
        await this.fetchClubs(this.pagination.currentPage + 1, this.pagination.pageSize)
      }
    },

    async prevPage() {
      if (this.pagination.previous) {
        await this.fetchClubs(this.pagination.currentPage - 1, this.pagination.pageSize)
      }
    },

    async goToPage(page: number) {
      if (page >= 1 && page <= this.totalPages) {
        await this.fetchClubs(page, this.pagination.pageSize)
      }
    },

    async changePageSize(size: number) {
      await this.fetchClubs(1, size)
    },

    async joinClub(clubId: number) {
      try {
        await axios.post(`/api/v1/clubs/${clubId}/members/me/`)
        await this.fetchClubs(this.pagination.currentPage, this.pagination.pageSize)
      } catch (error) {
        console.error('Error joining club:', error)
        throw error
      }
    },

    async leaveClub(clubId: number) {
      try {
        await axios.delete(`/api/v1/clubs/${clubId}/members/me/`)
        await this.fetchClubs(this.pagination.currentPage, this.pagination.pageSize)
      } catch (error) {
        console.error('Error leaving club:', error)
        throw error
      }
    },

    async fetchClub(clubId: number) {
      this.isLoading = true
      this.error = null
      try {
        const response = await axios.get(`/api/v1/clubs/${clubId}/`)
        return response.data
      } catch (error) {
        this.error = 'Не удалось загрузить информацию о клубе'
        console.error('Error fetching club:', error)
        throw error
      } finally {
        this.isLoading = false
      }
    },
  },

  getters: {
    totalPages(state): number {
      return Math.ceil(state.pagination.count / state.pagination.pageSize)
    },
    hasNextPage(state): boolean {
      return state.pagination.next !== null
    },
    hasPrevPage(state): boolean {
      return state.pagination.previous !== null
    },
    clubsCount(state): number {
      return state.clubs.length
    },
  },
})
