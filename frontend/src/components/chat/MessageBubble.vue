<template>
  <div class="flex gap-4" :class="role === 'user' ? 'flex-row-reverse' : ''">
    <div
      v-if="role === 'assistant'"
      class="w-10 h-10 bg-gradient-to-br from-teal-400 to-blue-500 rounded-full flex items-center justify-center text-white shadow-sm flex-shrink-0"
    >
      <AppIcon name="robot" />
    </div>
    <img
      v-else
      src="https://i.pravatar.cc/100?img=12"
      alt="用户头像"
      class="w-10 h-10 rounded-full border-2 border-white shadow-sm flex-shrink-0"
    >
    <div class="max-w-[80%]">
      <div
        :class="role === 'user' ? 'bg-white rounded-2xl rounded-tr-none' : 'bg-teal-50 border border-teal-100 rounded-2xl rounded-tl-none'"
        class="p-4 text-slate-700 shadow-sm prose prose-sm max-w-none prose-headings:font-bold prose-strong:text-slate-900"
      >
        <div class="whitespace-pre-wrap" v-html="formattedContent"></div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import AppIcon from '@/components/common/AppIcon.vue'

interface Props {
  role: 'user' | 'assistant'
  content: string
}

const props = defineProps<Props>()

const formattedContent = computed(() => {
  if (!props.content) return ''

  let formatted = props.content

  // 先清理不需要的字符和标记
  // 移除粘贴标记
  formatted = formatted.replace(/\[Pasted ~\d+ lines?\]/g, '')
  // 移除剪贴板标记
  formatted = formatted.replace(/\[Clipboard:\s*\d+ chars\]/g, '')
  // 移除Unicode引号，替换为普通引号
  formatted = formatted.replace(/"/g, '"')
  formatted = formatted.replace(/"/g, '"')
  formatted = formatted.replace(/'/g, "'")
  formatted = formatted.replace(/'/g, "'")

  // 转义HTML特殊字符（在格式化之前）
  formatted = formatted.replace(/&/g, '&amp;')
  formatted = formatted.replace(/</g, '&lt;')
  formatted = formatted.replace(/>/g, '&gt;')

  // 格式化Markdown标题
  formatted = formatted.replace(/^###\s+(.*$)/gim, '<h3 class="text-lg font-bold mt-3 mb-2 text-slate-800">$1</h3>')
  formatted = formatted.replace(/^##\s+(.*$)/gim, '<h2 class="text-xl font-bold mt-3 mb-2 text-slate-800">$1</h2>')
  formatted = formatted.replace(/^#\s+(.*$)/gim, '<h1 class="text-2xl font-bold mt-3 mb-2 text-slate-800">$1</h1>')

  // 格式化粗体文本 **text**
  formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')

  // 格式化斜体文本 *text*
  formatted = formatted.replace(/\*(?!\*)(.*?)\*(?!\*)/g, '<em>$1</em>')

  // 格式化分隔线
  formatted = formatted.replace(/^---$/gm, '<hr class="my-3 border-slate-200">')

  // 格式化表格 (简化版）
  formatted = formatted.replace(/\|(.+)\|/g, (match) => {
    const cells = match.split('|').filter(c => c.trim())
    if (cells.length > 1) {
      return '<div class="grid gap-2 my-2">' +
        cells.map(cell => `<div class="p-2 bg-slate-100 rounded">${cell.trim()}</div>`).join('') +
        '</div>'
    }
    return match
  })

  // 格式化列表项 - 无序列表
  formatted = formatted.replace(/^\s*[-*]\s+(.*$)/gim, '<div class="flex items-start gap-2 my-1"><span class="text-teal-500 mt-1">&bull;</span><span>$1</span></div>')

  // 格式化列表项 - 编号列表
  formatted = formatted.replace(/^\s*(\d+)\.\s+(.*$)/gim, '<div class="flex items-start gap-2 my-1"><span class="text-teal-500 mt-1 font-bold">$1.</span><span>$2</span></div>')

  // 处理段落（空行分隔）
  formatted = formatted.replace(/\n\n+/g, '</p><p class="mb-2">')

  // 包装整个内容
  formatted = `<p class="mb-0">${formatted}</p>`

  // 移除多余的段落标记
  formatted = formatted.replace(/<p class="mb-0"><\/p>/g, '')
  formatted = formatted.replace(/<p class="mb-2"><h/g, '<h')
  formatted = formatted.replace(/<\/h(\d)><\/p>/g, '</h$1>')

  // 移除连续的<br>
  formatted = formatted.replace(/<br\s*\/?><br\s*\/?>/g, '<br>')

  return formatted
})
</script>
