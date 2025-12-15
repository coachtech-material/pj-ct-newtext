# Tutorial 9-1-7: Laravel基礎 - ハンズオン演習

## 📝 このセクションの目的

Chapter 1で学んだLaravelの基礎を実際に手を動かして確認します。ルーティング、コントローラー、ビューの連携を実践しましょう。

---

## 🎯 演習課題：自己紹介ページを作成しよう

### 📋 要件

1. `/profile`にアクセスすると、自己紹介ページが表示される
2. `ProfileController`を作成する
3. `profile.blade.php`ビューを作成する
4. 名前、年齢、趣味を表示する

---

## 💡 ヒント

\`\`\`bash
php artisan make:controller ProfileController
\`\`\`

\`\`\`php
Route::get('/profile', [ProfileController::class, 'index']);
\`\`\`

---

## 📖 模範解答

### ProfileController.php

\`\`\`php
<?php

namespace App\Http\Controllers;

class ProfileController extends Controller
{
    public function index()
    {
        $data = [
            'name' => '山田太郎',
            'age' => 25,
            'hobbies' => ['プログラミング', '読書', '旅行'],
        ];
        
        return view('profile', $data);
    }
}
\`\`\`

### routes/web.php

\`\`\`php
use App\Http\Controllers\ProfileController;

Route::get('/profile', [ProfileController::class, 'index']);
\`\`\`

### profile.blade.php

\`\`\`blade
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>プロフィール</title>
</head>
<body>
    <h1>プロフィール</h1>
    <p>名前: {{ \$name }}</p>
    <p>年齢: {{ \$age }}歳</p>
    <p>趣味:</p>
    <ul>
        @foreach (\$hobbies as \$hobby)
            <li>{{ \$hobby }}</li>
        @endforeach
    </ul>
</body>
</html>
\`\`\`

---

## 💪 自己評価チェックリスト

- [ ] コントローラーを作成できた
- [ ] ルーティングを定義できた
- [ ] ビューを作成できた
- [ ] データを渡せた

すべてチェックできたら、Chapter 2に進みましょう！
