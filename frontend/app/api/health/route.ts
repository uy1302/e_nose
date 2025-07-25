export async function GET() {
  try {
    const backendUrl = process.env.BACKEND_API_URL || 'http://localhost:5000'

    const response = await fetch(`${backendUrl}/health`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ error: 'Unknown error' }))
      throw new Error(errorData.error || `Backend API error: ${response.status}`)
    }

    const apiResponse = await response.json()
    
    // Add NextJS frontend info to health response
    const healthResponse = {
      ...apiResponse,
      frontend: {
        status: 'healthy',
        service: 'NextJS Frontend',
        version: '1.0.0',
        backend_url: backendUrl,
      }
    }
    
    return Response.json(healthResponse)

  } catch (error) {
    console.error('Health API error:', error)
    
    // Return backend connection error with frontend status
    return Response.json(
      {
        status: 'degraded',
        service: 'E-Nose System',
        frontend: {
          status: 'healthy',
          service: 'NextJS Frontend',
          version: '1.0.0',
        },
        backend: {
          status: 'unhealthy',
          error: error instanceof Error ? error.message : 'Backend connection failed',
        },
        timestamp: new Date().toISOString(),
      }, 
      { status: 503 }
    )
  }
} 