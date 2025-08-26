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
    async fetchClubs(page: number = 1, pageSize: number = 10) {
      this.isLoading = true
      this.error = null
      try {
        const response = await axios.get<PaginatedClubList>(
          `/api/v1/clubs/?page=${page}&page_size=${pageSize}`,
        )
        this.clubs = response.data.results
        this.pagination = {
          count: response.data.count,
          next: response.data.next,
          previous: response.data.previous,
          currentPage: page,
          pageSize: pageSize,
        }
      } catch (error) {
        this.error = 'Не удалось загрузить список клубов'
        console.error('Error fetching clubs:', error)
      } finally {
        this.isLoading = false
      }
    },

    async searchClubs(query: string, page: number = 1, pageSize: number = 10) {
      this.isLoading = true
      this.error = null
      try {
        const response = await axios.get<PaginatedClubList>(
          `/api/v1/clubs/?search=${encodeURIComponent(query)}&page=${page}&page_size=${pageSize}`,
        )
        this.clubs = response.data.results
        this.pagination = {
          count: response.data.count,
          next: response.data.next,
          previous: response.data.previous,
          currentPage: page,
          pageSize: pageSize,
        }
      } catch (error) {
        this.error = 'Ошибка при поиске клубов'
        console.error('Error searching clubs:', error)
      } finally {
        this.isLoading = false
      }
    },

    async filterByMembership(
      type: 'member' | 'owner' | 'all',
      page: number = 1,
      pageSize: number = 10,
    ) {
      this.isLoading = true
      this.error = null
      try {
        let url = `/api/v1/clubs/`
        if (type !== 'all') {
          url += `?membership=${type}&page=${page}&page_size=${pageSize}`
        } else {
          url += `?page=${page}&page_size=${pageSize}`
        }

        const response = await axios.get<PaginatedClubList>(url)
        this.clubs = response.data.results
        this.pagination = {
          count: response.data.count,
          next: response.data.next,
          previous: response.data.previous,
          currentPage: page,
          pageSize: pageSize,
        }
      } catch (error) {
        this.error = 'Ошибка при фильтрации клубов'
        console.error('Error filtering clubs:', error)
      } finally {
        this.isLoading = false
      }
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
