import { NextResponse } from 'next/server'
 
export async function middleware(request) {
  // const tokenStatus = await fetch('https://api.example.com/token-status');
  const tokenStatus = 'good';
  if (tokenStatus === 'expired') {
    return NextResponse.redirect(new URL('/login', request.url))
  }
  return NextResponse.next();
}
 
export const config = {
  matcher: '/((?!api|_next/static|_next/image|favicon.ico|login).*)',
}