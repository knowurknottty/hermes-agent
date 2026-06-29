import { atom } from 'nanostores'

import { getLearningGraph } from '@/hermes'
import type { LearningGraph } from '@/types/hermes'

// On-demand cache for the learning panel. The graph scan touches the skills
// catalog + usage ledger + memory files, so we fetch it only when the panel
// opens (and on an explicit refresh), never on a turn boundary.
export const $learningGraph = atom<LearningGraph | null>(null)
export const $learningLoading = atom(false)
export const $learningError = atom<null | string>(null)

let inflight: Promise<void> | null = null

export async function loadLearningGraph(force = false): Promise<void> {
  if (inflight) {
    return inflight
  }

  if ($learningGraph.get() && !force) {
    return
  }

  $learningLoading.set(true)
  $learningError.set(null)

  inflight = (async () => {
    try {
      $learningGraph.set(await getLearningGraph())
    } catch (err) {
      $learningError.set(err instanceof Error ? err.message : String(err))
    } finally {
      $learningLoading.set(false)
      inflight = null
    }
  })()

  return inflight
}

/** Drop the cache so the next open refetches against the now-active profile. */
export function resetLearningGraph(): void {
  inflight = null
  $learningGraph.set(null)
  $learningError.set(null)
}
