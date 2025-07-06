export async function GET() {
  try {
    const backendUrl = process.env.BACKEND_API_URL || 'http://localhost:5000'

    const response = await fetch(`${backendUrl}/models`, {
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
    return Response.json(apiResponse)

  } catch (error) {
    console.error('Models API error:', error)
    
    // Return detailed error message
    const errorMessage = error instanceof Error 
      ? error.message 
      : 'Có lỗi xảy ra khi tải thông tin mô hình'
    
    return Response.json(
      { error: errorMessage }, 
      { status: 500 }
    )
  }
}
