import { useEffect } from 'react';
import { useRouter } from 'next/router';
// TEMPORARY: Authentication disabled - redirect to standalone
// import { isAuthenticated, getRole, getRedirectPath } from '@/lib/auth';

export default function Home() {
  const router = useRouter();

  useEffect(() => {
    // TEMPORARY: Direct redirect to standalone (authentication disabled)
    router.push('/standalone');
    
    /* ORIGINAL CODE - DISABLED
    if (isAuthenticated()) {
      const role = getRole();
      if (role) {
        router.push(getRedirectPath(role));
      } else {
        router.push('/login');
      }
    } else {
      router.push('/login');
    }
    */
  }, [router]);

  return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="text-lg">Redirecting...</div>
    </div>
  );
}

