# 9-1-3: Laravelリクエストライフサイクル

## プロンプト本文

```
Create a detailed educational infographic showing the complete request lifecycle
in Laravel's MVC architecture, designed for Japanese programming students.

Title at top: "Laravel リクエストライフサイクル" in bold dark text.

Show a numbered step-by-step flow arranged in an S-curve pattern:

Step 1 (top-left): ユーザーがブラウザでURLにアクセス
- Icon: person with laptop

Step 2: リクエストがルーティングに到達 (routes/web.php)
- Icon: signpost/routing symbol
- Small code snippet: Route::get('/users', [UserController::class, 'index'])

Step 3: コントローラーが呼び出される (app/Http/Controllers/)
- Icon: gear/cog
- Text: リクエストを受け取り、ビジネスロジックを実行

Step 4: モデルがデータベースと通信 (app/Models/)
- Icon: database cylinder
- Text: Eloquent ORMでデータを取得・保存

Step 5: ビューがHTMLを生成 (resources/views/)
- Icon: browser window
- Text: Bladeテンプレートでデータを表示

Step 6 (bottom-right): レスポンスがユーザーに返される
- Icon: same person with laptop, now with a smile

Connect all steps with smooth curved arrows. Each step should be in a distinct
colored card (use a palette of: coral, amber, sky blue, mint green, lavender,
and warm gray).

Style: Modern, clean infographic with rounded cards, soft shadows, and clear
Japanese typography. White background. Professional but approachable.
Format: 9:16 (vertical/portrait)
```
