param(
  [string]$BaseUrl = "http://localhost:8000",
  [string]$Email = "guest@wanderflow.app",
  [string]$Password = "guest",
  [string]$Query = "请根据澳门旅游攻略回答：澳门有哪些必去景点？"
)

$loginBody = @{ email = $Email; password = $Password } | ConvertTo-Json
$login = Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/auth/login" -Body $loginBody -ContentType "application/json"
if (-not $login.access_token) {
  Write-Error "Login failed: missing access_token"
  exit 1
}

$headers = @{ Authorization = "Bearer $($login.access_token)" }

function Invoke-QA {
  param(
    [bool]$KnowledgeBaseEnabled,
    [string]$Label
  )

  $sessionBody = @{
    title = "KB Smoke Test - $Label"
    features = @{
      knowledge_base = $KnowledgeBaseEnabled
      weather = $false
      voice = $false
    }
  } | ConvertTo-Json

  $session = Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/qa/sessions" -Headers $headers -Body $sessionBody -ContentType "application/json"
  $sessionId = $session.data.session.id
  if (-not $sessionId) {
    Write-Error "Create session failed: missing session id"
    exit 1
  }

  $messageBody = @{
    content = $Query
    session_id = $sessionId
    message_type = "text"
  } | ConvertTo-Json

  $reply = Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/qa/messages" -Headers $headers -Body $messageBody -ContentType "application/json"
  $assistant = $reply.data.message.content

  if (-not $assistant) {
    Write-Error "QA reply is empty"
    exit 1
  }

  Write-Host "==== $Label ===="
  Write-Host "Session: $sessionId"
  Write-Host "Question: $Query"
  Write-Host "Answer:"
  Write-Host $assistant
  Write-Host ""
}

Invoke-QA -KnowledgeBaseEnabled $false -Label "No KB"
Invoke-QA -KnowledgeBaseEnabled $true -Label "With KB"
