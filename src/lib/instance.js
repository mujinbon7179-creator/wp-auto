// Instance mode detection
// Central: NEXT_PUBLIC_INSTANCE_MODE=central (set on planxs-ai Vercel)
// Self-hosted: not set (default for forks)

export function getInstanceMode() {
  return process.env.NEXT_PUBLIC_INSTANCE_MODE === 'central' ? 'central' : 'selfhosted';
}

export function isCentral() {
  return getInstanceMode() === 'central';
}

export function isSelfHosted() {
  return getInstanceMode() === 'selfhosted';
}
