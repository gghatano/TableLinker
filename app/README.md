# Vue 3 + Typescript + Vite

This template should help get you started developing with Vue 3 and Typescript in Vite. The template uses Vue 3 `<script setup>` SFCs, check out the [script setup docs](https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup) to learn more.

## Recommended IDE Setup

- [VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=johnsoncodehk.volar)

## GraphQL の反映

GraphQLAPI への変更の方法を記載する

### 1.GraphQL ファイルの書き換え

`src/app/graphql`内にある GraphQL ファイルを変更する

カラムの追加や Query/Mutaion の追加など変更したい内容をファイルに反映させてください。

### 2.コード生成

ローカルの API サーバを起動した状態で、以下のコマンドを実行してください。

```
cd src/app
yarn codegen
```

以下のコードにコードが生成されます。

```
src/app/modules/graphql.ts
```

### 3.生成されたコードを使って実装

以下の名前で、型やコードが生成されるので、使用してコードを実装する

```
use<GraphQLのQuery/Mutaion名前>
```
