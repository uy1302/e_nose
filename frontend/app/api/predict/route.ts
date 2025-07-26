import { NextResponse } from 'next/server'

export async function POST(request: Request) {
  try {
    const body = await request.json()
    const backendUrl = process.env.BACKEND_API_URL || 'http://localhost:5000'

    // Validate sensor data
    if (!body.sensor_data || !Array.isArray(body.sensor_data) || body.sensor_data.length !== 4) {
      return NextResponse.json(
        { 
          error: 'sensor_data phải chứa đúng 4 giá trị', 
          received: body.sensor_data?.length || 0,
          expected: 4,
          sensor_names: ['MQ136', 'MQ137', 'TEMP', 'HUMI']
        },
        { status: 400 }
      )
    }

    const response = await fetch(`${backendUrl}/predict`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        sensor_data: body.sensor_data,
      }),
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ error: 'Unknown error' }))
      throw new Error(errorData.error || `Backend API error: ${response.status}`)
    }

    const apiResponse = await response.json()
    return Response.json(apiResponse)

  } catch (error) {
    console.error('Prediction API error:', error)
    
    // Return detailed error message
    const errorMessage = error instanceof Error 
      ? error.message 
      : 'Có lỗi xảy ra khi xử lý dự đoán'
    
    return Response.json(
      { error: errorMessage }, 
      { status: 500 }
    )
  }
}
