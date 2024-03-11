import type { APIGatewayProxyEventV2, APIGatewayProxyResultV2, Context } from 'aws-lambda'
import QRCode from 'qrcode'

export async function handler(
  event: APIGatewayProxyEventV2,
  context: Context
): Promise<APIGatewayProxyResultV2> {
  console.log(context.functionName)
  console.log(await QRCode.toString(context.functionName, { type: 'terminal' }))
  return {
    statusCode: 200,
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify(event, null, 2),
  }
}
