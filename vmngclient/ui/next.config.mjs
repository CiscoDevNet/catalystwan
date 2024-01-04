/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: false,
  pageExtensions: ["ts", "tsx", "js", "jsx", "mdx"],
  experimental: {
    scrollRestoration: true,
    // appDir: true
  },
  eslint: {
    // Warning: This allows production builds to successfully complete even if
    // your project has ESLint errors.
    ignoreDuringBuilds: true,
  },
  images: {
    unoptimized: true,
  },
  async redirects() {
    return [
      {
        source: "/dev/workflows/create-site",
        destination: "/dev/workflows/create-site/name-site",
        permanent: true,
      },
    ];
  }
};

export default nextConfig;