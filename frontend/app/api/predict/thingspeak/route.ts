export async function POST(request: Request) {
  try {
    const body = await request.json()
    const backendUrl = process.env.BACKEND_API_URL || 'http://localhost:5000'

    const response = await fetch(`${backendUrl}/predict`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        api_key: body.api_key,
      }),
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ error: 'Unknown error' }))
      throw new Error(errorData.error || `Backend API error: ${response.status}`)
    }

    const apiResponse = await response.json()
    return Response.json(apiResponse)

  } catch (error) {
    console.error('ThingSpeak Prediction API error:', error)
    
    // Return detailed error message
    const errorMessage = error instanceof Error 
      ? error.message 
      : 'Có lỗi xảy ra khi kết nối ThingSpeak'
    
    return Response.json(
      { error: errorMessage }, 
      { status: 500 }
    )
  }
}
