import { useCallback, useEffect, useState } from "react";

interface AsyncState<T> {
  data: T | undefined;
  error: string | undefined;
  loading: boolean;
  reload: () => void;
}

interface Settled<T> {
  key: string;
  data: T | undefined;
  error: string | undefined;
}

/**
 * Runs `fn` whenever `deps` change. Stale responses are ignored (last request wins) and the
 * previous data stays visible while a new request is in flight. `loading` is derived by
 * comparing the settled request key with the current one, so no setState happens in the effect body.
 */
export function useAsync<T>(fn: () => Promise<T>, deps: unknown[]): AsyncState<T> {
  const [tick, setTick] = useState(0);
  const [settled, setSettled] = useState<Settled<T>>();
  const key = JSON.stringify([...deps, tick]);

  useEffect(() => {
    let cancelled = false;
    fn()
      .then((data) => !cancelled && setSettled({ key, data, error: undefined }))
      .catch((e: Error) =>
        !cancelled && setSettled((prev) => ({ key, data: prev?.data, error: e.message })),
      );
    return () => {
      cancelled = true;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [key]);

  const reload = useCallback(() => setTick((t) => t + 1), []);
  return {
    data: settled?.data,
    error: settled?.error,
    loading: settled?.key !== key,
    reload,
  };
}
