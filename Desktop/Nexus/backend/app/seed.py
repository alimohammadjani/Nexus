"""Seed demo data on first startup."""

import logging

from sqlalchemy import select

from app.core.security import hash_password
from app.database import SessionLocal
from app.models.job import Job
from app.models.learning import Course, CourseEnrollment, Lesson, Roadmap, RoadmapStage
from app.models.market import Order, Product
from app.models.payment import Payment, Transaction
from app.models.user import Skill, User

logger = logging.getLogger("devhub.seed")


# ---------------------------------------------------------------------------
# Roadmap definitions — each stage carries COMPLETE, accurate training content
# (Persian with English technical terms), curated resource links, a hands-on
# project and a self-check checkpoint.
# ---------------------------------------------------------------------------

ROADMAPS: dict[str, dict] = {
    "frontend": {
        "title": "توسعه‌دهنده Frontend",
        "subtitle": "از HTML تا انتشار اپلیکیشن‌های واکنش‌گرا با React و TypeScript",
        "description": "مسیر کامل ساخت رابط‌های کاربری مدرن: ساختار، استایل، منطق، فریم‌ورک و انتشار.",
        "category": "frontend",
        "color": "#06b6d4",
        "stages": [
            {
                "order": 1,
                "title": "HTML و وب معنایی",
                "description": "ساختار صفحات وب با تگ‌های معنایی و دسترس‌پذیری.",
                "content": '''## یادگیری در یک نگاه
HTML زیربنای هر صفحه وب است. هدف این مرحله ساختن سندی است که «معنی» محتوا را با تگ درست مشخص کند — نه فقط ظاهر آن را. ساختار درست پایهٔ سئو، دسترس‌پذیری و نگهداری آسان است.

## مفاهیم کلیدی
- تگهای معنایی: `<header>`, `<nav>`, `<main>`, `<article>`, `<section>`, `<footer>` در برابر استفادهٔ بی‌رویه از `<div>`
- دسترس‌پذیری: متن `alt` برای تصاویر، `<label>` برای ورودی‌ها، نقش‌های `aria-*`
- سلسله‌مراتب عنوان‌ها: فقط یک `<h1>` در هر صفحه و رعایت ترتیب h2 → h3
- فرم‌ها و انواع `input` (`text`, `email`, `number`, `date`) به همراه اعتبارسنجی HTML5
- تفاوت المان‌های block (مثل `p`) و inline (مثل `span`)

## گام‌به‌گام
1. فایل `index.html` بسازید و ساختار پایه (`<!doctype html>`, `head`, `body`) را بنویسید.
2. محتوا را با تگهای معنایی بپوشانید: یک `header` با ناوبری، یک `main` برای محتوای اصلی و یک `footer`.
3. فرم تماس با فیلدهای نام، ایمیل و پیام اضافه کنید و با `required` اعتبارسنجی کنید.
4. سطح دسترس‌پذیری را با Lighthouse یا افزونه axe بررسی کنید.

## مثال
```html
<main>
  <article>
    <h1>عنوان پست</h1>
    <img src="cover.jpg" alt="تصویر کاور پست" />
    <p>متن پست که با معنا نوشته شده است.</p>
  </article>
</main>
```

> همیشه برای تصاویر متن `alt` بنویسید؛ این تنها راهی است که کاربر نابینا از محتوای تصویر آگاه می‌شود.

## اشتباهات رایج
- استفاده از `<div onclick>` به‌جای دکمه واقعی `<button>` — دکمه رفتار کیبورد و دسترس‌پذیری را رایگان می‌دهد.
- چندین `<h1>` در یک صفحه که سلسله‌مراتب را خراب می‌کند.

## تمرین
صفحه پروفایل شخصی بسازید با بخش دربارهٔ من، لیست مهارت‌ها و فرم تماس، طوری که در اعتبارسنجی HTML خطای ساختاری نداشته باشد.''',
                "resources": "MDN HTML — https://developer.mozilla.org/ru/docs/Web/HTML, web.dev Learn HTML — https://web.dev/learn/html, W3C Validator — https://validator.w3.org",
                "project": "ساخت یک صفحه پروفایل شخصی معنایی با فرم تماس و نقشه.",
                "checkpoint": "اعتبارسنجی HTML خطای ساختاری ندارد و با صفحه‌خوان تست می‌شود.",
            },
            {
                "order": 2,
                "title": "CSS و چیدمان (Flexbox / Grid)",
                "description": "ظاهر و چیدمان صفحه با باکس‌مدل و سیستم‌های مدرن چیدمان.",
                "content": '''## یادگیری در یک نگاه
CSS ظاهر صفحه را می‌سازد. امروزه تقریباً تمام چیدمان‌ها با Flexbox و CSS Grid حل می‌شوند؛ درک درست باکس‌مدل و این دو سیستم یعنی دیگر نیازی به کتابخانه‌های سنگین چیدمان ندارید.

## مفاهیم کلیدی
- **Box model**: `content`, `padding`, `border`, `margin` و نحوه محاسبهٔ عرض واقعی
- Flexbox برای چیدمان یک‌بعدی (یک ردیف یا ستون) با `justify-content` و `align-items`
- Grid برای چیدمان دوبعدی (کل صفحات) با `grid-template-columns` و `fr`
- واحدهای نسبی: `rem`, `em`, `%`, `vh/vw`, و تابع `clamp()`
- ریسپانسیو با media queries و رویکرد mobile-first

## گام‌به‌گام
1. باکس‌مدل را با تغییر `padding` و `border` یک المان آزمایش کنید.
2. یک نوار ابزار را با Flexbox بچینید (پخش فضا با `gap` و `space-between`).
3. یک گالری را با Grid و ستون‌های خودکار (`repeat(auto-fill, minmax(200px, 1fr))`) بسازید.
4. با media query حالت موبایل (≤۳۲۰px) را تنظیم کنید.

## مثال
```css
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
}
```

> برای چیدمان کل صفحه همیشه Grid را ترجیح دهید؛ Flexbox بهترین گزینه برای اجزای کوچک‌تر است.

## اشتباهات رایج
- استفاده از `position: absolute` برای چیدمان کل صفحه — این صفحه را شکننده می‌کند.
- فراموش کردن `box-sizing: border-box` که محاسبهٔ ابعاد را ساده می‌کند.

## تمرین
صفحه پروفایل قبلی را با Grid بچینید و مطمئن شوید در عرض ۳۲۰px و ۱۲۸۰px یکسان و تمیز است.''',
                "resources": "CSS Tricks Flexbox — https://css-tricks.com/snippets/css/a-guide-to-flexbox, CSS Tricks Grid — https://css-tricks.com/snippets/css/complete-guide-grid, web.dev Learn CSS — https://web.dev/learn/css",
                "project": "بازسازی صفحه پروفایل با Grid و نسخه موبایل (≤۳۲۰px).",
                "checkpoint": "صفحه در عرض ۳۲۰px و ۱۲۸۰px یکسان و تمیز است.",
            },
            {
                "order": 3,
                "title": "JavaScript — مبانی",
                "description": "زبان رفتار صفحه را قبل از هر فریم‌ورکی یاد بگیرید.",
                "content": '''## یادگیری در یک نگاه
JavaScript رفتار صفحه را می‌سازد. درک درست زبان — انواع، توابع، آرایه‌ها و DOM — پیش‌نیاز ضروری هر فریم‌ورکی مثل React است.

## مفاهیم کلیدی
- انواع داده: `string`, `number`, `boolean`, `null`, `undefined`, `object`, `array`
- توابع، حوزهٔ دسترسی (scope) و closures
- حلقه‌ها (`for`, `for...of`) و شرط‌ها
- متدهای پرکاربرد آرایه: `map`, `filter`, `reduce`, `find`, `some`
- DOM: انتخاب عناصر (`querySelector`)، تغییر محتوا و گوش‌دادن به رویدادها (event listeners)

## گام‌به‌گام
1. یک آرایه از کارها بسازید و با `map` خروجی HTML تولید کنید.
2. با `addEventListener` به کلیک یک دکمه گوش دهید.
3. وضعیت را در یک متغیر نگه دارید و لیست را بعد از هر تغییر دوباره رندر کنید.
4. داده را در `localStorage` ذخیره و هنگام بارگذاری بخوانید.

## مثال
```js
const tasks = ['یادگیری JS', 'تمرین DOM'];
tasks.map((t) => `<li>${t}</li>`).join('');
```

> متدهای آرایه مثل `map` و `filter` «غیرمخرب» (immutable) هستند: آرایهٔ اصلی را تغییر نمی‌دهند.

## اشتباهات رایج
- استفاده از `var` به‌جای `let`/`const` که باعث باگ‌های حوزهٔ دسترسی می‌شود.
- فراموش کردن اینکه `const` مانع تغییر «مقدار» نیست، فقط مانع تخصیص مجدد مرجع است.

## تمرین
یک To-Do list تعاملی بسازید که افزودن/حذف کار کند و لیست را در localStorage ذخیره کند.''',
                "resources": "javascript.info — https://javascript.info, MDN JavaScript — https://developer.mozilla.org/ru/docs/Web/JavaScript, Eloquent JS — https://eloquentjavascript.net",
                "project": "ساخت یک To-Do list تعاملی با ذخیره در localStorage.",
                "checkpoint": "اپ To-Do بدون بازنویسی صفحه (بدون reload) کار می‌کند.",
            },
            {
                "order": 4,
                "title": "JavaScript مدرن (ES6+)",
                "description": "ابزارهای نسخه‌های جدید که کد را خواناتر می‌کنند.",
                "content": '''## یادگیری در یک نگاه
نسخه‌های جدید JavaScript (ES2015 به بعد) ابزارهایی دارند که خوانایی، ایمنی و نگهداری کد را بهبود می‌دهند. اکثر کدهای امروزی روی این نسخه‌ها می‌چرخند.

## مفاهیم کلیدی
- `let`/`const` و تفاوت آن‌ها با `var`
- arrow functions و رفتار `this` در آن‌ها
- template literals با `` ` `` برای رشته‌های چندخطی و درج متغیر
- destructuring و spread/rest (`...`)
- modules با `import`/`export`
- `async/await` و Promiseها برای کار با شبکه

## گام‌به‌گام
1. یک تابع سنتی را به arrow function تبدیل کنید.
2. یک آبجکت را با destructuring باز کنید و آرایه‌ای را با spread ترکیب کنید.
3. یک تابع `async` بنویسید که با `await` داده از یک API دریافت کند.
4. خطاها را با `try/catch` مدیریت کنید.

## مثال
```js
const getUser = async (id) => {
  const res = await fetch(`/api/users/${id}`);
  return res.json();
};
```

> با `await` کد غیرهمزمان دقیقاً مثل کد همزمان خوانده می‌شود؛ دیگر نیازی به زنجیرهٔ `.then()` نیست.

## اشتباهات رایج
- استفاده از `await` خارج از تابع `async` که خطای نحوی می‌دهد.
- فراموش کردن مدیریت خطا در درخواست‌های شبکه.

## تمرین
یک API عمومی (مثل JSONPlaceholder) را فراخوانی کنید و لیستی از آیتم‌ها را با `async/await` نمایش دهید.''',
                "resources": "MDN ES6 — https://developer.mozilla.org/ru/docs/Web/JavaScript/New_in_JavaScript/ECMAScript_2015, javascript.info/async — https://javascript.info/async-await",
                "project": "فراخوانی یک API عمومی و نمایش لیست با async/await.",
                "checkpoint": "داده‌ها بدون callback nesting (پیرامون callback) دریافت می‌شوند.",
            },
            {
                "order": 5,
                "title": "TypeScript",
                "description": "نسخه ایمن‌تر JS که در پروژه‌های بزرگ استاندارد شده.",
                "content": '''## یادگیری در یک نگاه
TypeScript نوع‌های ایستا اضافه می‌کند تا باگ‌ها قبل از اجرا، هنگام کامپایل گرفته شوند. این ویژگی در پروژه‌های تیمی و بزرگ ارزشمند است.

## مفاهیم کلیدی
- انواع پایه (`string`, `number`, `boolean`) و استنتاج نوع (type inference)
- `interface` و `type` برای مدل‌سازی داده
- genericها `<T>` برای کدِ قابل‌استفادهٔ مجدد
- utility types: `Partial`, `Pick`, `Omit`, `Record`
- تنظیم `tsconfig.json` و یکپارچه‌سازی با ابزار بسته‌بندی

## گام‌به‌گام
1. یک پروژه کوچک را با `tsc --init` راه‌اندازی کنید.
2. یک `interface User` تعریف کنید و تابعی بنویسید که آن را می‌پذیرد.
3. یک تابع generic بنویسید که روی هر آرایه‌ای کار کند.
4. خطای نوع عمدی ایجاد کنید تا رفتار کامپایلر را ببینید.

## مثال
```ts
interface User { id: number; name: string }
const greet = (u: User) => `سلام ${u.name}`;
```

> هدف TypeScript صفر کردن خطاهای نوع نیست، بلکه مستندسازی قراردادهای داده با خود کامپایلر است.

## اشتباهات رایج
- استفاده بیش از حد از `any` که تمام مزایای نوع را از بین می‌برد.
- نادیده گرفتن پیام‌های کامپایلر به امید «اجرای درست».

## تمرین
To-Do list قبلی را به TypeScript بازنویسی کنید با تایپ‌های صریح و یک `interface Task`.''',
                "resources": "TypeScript Handbook — https://www.typescriptlang.org/docs/handbook/intro.html, Type Challenges — https://github.com/type-challenges/type-challenges",
                "project": "بازنویسی To-Do list با تایپ‌های صریح و interfaceها.",
                "checkpoint": "کامپایلر TS بدون خطای نوع (type error) عبور می‌کند.",
            },
            {
                "order": 6,
                "title": "React — پایه (Components & Hooks)",
                "description": "کتابخانه ساخت رابط کاربری بر پایه کامپوننت.",
                "content": '''## یادگیری در یک نگاه
React UI را به کامپوننت‌های کوچک و قابل‌استفاده تقسیم می‌کند. ایدهٔ مرکزی این است: شما «چه چیزی» می‌خواهید نشان دهید را توصیف می‌کنید و React DOM را به‌روزرسانی می‌کند.

## مفاهیم کلیدی
- JSX و تفاوت آن با HTML (مثلاً `className` به‌جای `class`)
- `props` برای ورودی و `state` برای دادهٔ داخلی
- hooks پایه: `useState`, `useEffect`, `useRef`
- رندر لیست‌ها و اهمیت کلید (`key`) منحصربه‌فرد
- مدیریت فرم‌ها در React (controlled inputs)

## گام‌به‌گام
1. یک کامپوننت `Counter` با `useState` بسازید.
2. لیستی از آیتم‌ها را با `.map` رندر کنید و `key` بدهید.
3. با `useEffect` یک پیام خوش‌آمدگویی هنگام mount نمایش دهید.
4. مقدار یک input را در state نگه دارید.

## مثال
```tsx
function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(count + 1)}>{count}</button>;
}
```

> در React مستقیماً DOM را تغییر ندهید؛ به‌جای آن state را عوض کنید و اجازه دهید React رندر را همگام کند.

## اشتباهات رایج
- استفاده از index آرایه به‌عنوان `key` که در لیست‌های تغییرپذیر باعث باگ می‌شود.
- تغییر دادن state به‌صورت جایگزینی اشتباه (همیشه نسخهٔ جدید بسازید).

## تمرین
یک برنامه آب‌وهوا با کامپوننت‌های قابل‌استفاده بسازید که state بدون دستکاری دستی DOM به‌روز شود.''',
                "resources": "React Learn — https://react.dev/learn, React Hooks — https://react.dev/reference/react",
                "project": "ساخت یک برنامه آب‌وهوا با کامپوننت‌های قابل‌استفاده.",
                "checkpoint": "state بدون دستکاری دستی DOM به‌روز می‌شود.",
            },
            {
                "order": 7,
                "title": "مدیریت وضعیت و دریافت داده",
                "description": "وضعیت سراسری و همگام‌سازی با سرور در اپلیکیشن‌های بزرگ.",
                "content": '''## یادگیری در یک نگاه
با بزرگ‌شدن اپ، مدیریت وضعیت و دادهٔ سرور اهمیت پیدا می‌کند. ابزارهایی مثل TanStack Query تکرار درخواست، کش و همگام‌سازی را مدیریت می‌کنند.

## مفاهیم کلیدی
- data fetching در کلاینت و مدیریت وضعیت‌های loading/error/success
- کتابخانه‌هایی مثل TanStack Query برای کش و همگام‌سازی
- مدیریت وضعیت سراسری با Context یا Zustand
- بهینه‌سازی رندر با `useMemo` و `useCallback`
- الگوهای optimistic update (به‌روزرسانی خوش‌بینانه)

## گام‌به‌گام
1. با `fetch` داده را در `useEffect` بگیرید و در state ذخیره کنید.
2. وضعیت‌های loading و error را در رابط نشان دهید.
3. درخواست‌ها را با TanStack Query جایگزین کنید تا کش شوند.
4. فرم جستجو بسازید که نتایج را فیلتر کند.

## مثال
```tsx
const { data, isLoading } = useQuery({
  queryKey: ['users'],
  queryFn: () => fetch('/api/users').then(r => r.json()),
});
```

> هر state را سراسری (global) نکنید؛ فقط داده‌هایی را سراسری کنید که واقعاً بین چند کامپوننت غیرمرتبط مشترک‌اند.

## اشتباهات رایج
- قرار دادن تمام state در یک store بزرگ که رندرهای غیرضروری ایجاد می‌کند.
- نادیده گرفتن وضعیت loading/error در رابط کاربری.

## تمرین
به اپ آب‌وهوا جستجو و فیلتر اضافه کنید و درخواست‌های تکراری را کش کنید.''',
                "resources": "TanStack Query — https://tanstack.com/query/latest, React data — https://react.dev/learn, Zustand — https://github.com/pmndrs/zustand",
                "project": "افزودن جستجو و فیلتر به اپ آب‌وهوا با کش کردن درخواست‌ها.",
                "checkpoint": "درخواست‌های تکراری کش می‌شوند و اپ در آفلاین واکنش درستی دارد.",
            },
            {
                "order": 8,
                "title": "ابزارها، عملکرد و انتشار",
                "description": "بسته‌بندی، بهینه‌سازی، تست و استقرار.",
                "content": '''## یادگیری در یک نگاه
قبل از انتشار باید پروژه را بسته‌بندی، بهینه و تست کنید. این مرحله تفاوت بین یک نمونهٔ آزمایشی و یک محصول واقعی است.

## مفاهیم کلیدی
- Vite یا Next.js برای بسته‌بندی و (در صورت نیاز) رندر سمت سرور (SSR)
- کاهش حجم باندل: code splitting و lazy loading
- دسترس‌پذیری و سئو (meta tags، ساختار معنایی)
- تست واحد با Vitest و تست end-to-end با Playwright
- استقرار روی Vercel / Netlify / GitHub Pages

## گام‌به‌گام
1. پروژه را با `vite build` بسته‌بندی کنید و حجم باندل را ببینید.
2. یک کامپوننت سنگین را با `React.lazy` بارگذاری تنبل کنید.
3. یک تست واحد برای تابع محاسباتی بنویسید.
4. پروژه را روی Vercel با اتصال به مخزن GitHub منتشر کنید.

## مثال
```tsx
const Chart = React.lazy(() => import('./Chart'));
```

> Lighthouse را قبل و بعد از بهینه‌سازی اجرا کنید؛ عددهای عملکرد هدایت‌کنندهٔ بهتری از حدس زدن هستند.

## اشتباهات رایج
- بارگذاری همهٔ کتابخانه‌ها در ابتدای برنامه (باندل بزرگ).
- انتشار بدون تست که باعث خرابی در تولید می‌شود.

## تمرین
اپ آب‌وهوا را روی Vercel منتشر کنید و نمرهٔ Lighthouse عملکرد را بالای ۹۰ برسانید.''',
                "resources": "Vite — https://vitejs.dev, Next.js — https://nextjs.org/docs, web.dev Measure — https://web.dev/measure, Vitest — https://vitest.dev",
                "project": "انتشار اپ آب‌وهوا روی Vercel با یک خط لوله CI.",
                "checkpoint": "نمره Lighthouse در عملکرد بالای ۹۰ است.",
            },
        ],
    },
    "backend": {
        "title": "توسعه‌دهنده Backend",
        "subtitle": "از مبانی زبان تا APIهای تولیدی و استقرار با کانتینر",
        "description": "مسیر ساخت سرویس‌های سمت سرور: زبان، پایگاه‌داده، API، امنیت و عملیات.",
        "category": "backend",
        "color": "#8b5cf6",
        "stages": [
            {
                "order": 1,
                "title": "مبانی زبان (Python)",
                "description": "درک زبان میزبان قبل از فریم‌ورک‌ها.",
                "content": '''## یادگیری در یک نگاه
Python به دلیل خوانایی و اکوسیستم گسترده برای بک‌اند محبوب است. درک درست زبان پیش‌نیاز استفادهٔ درست از فریم‌ورک‌هاست.

## مفاهیم کلیدی
- انواع داده و تفاوت mutable/immutable (مثلاً لیست در برابر تاپل)
- توابع، decoratorها و generatorها
- مدیریت خطا با `try/except/finally`
- ماژول‌ها، packages و virtual environments (`venv`, `pip`)
- تایپینگ ایستا با ماژول `typing` و ابزار `mypy`

## گام‌به‌گام
1. یک محیط مجازی با `python -m venv .venv` بسازید و فعال کنید.
2. یک تابع با decorator بنویسید که زمان اجرا را اندازه‌گیری کند.
3. خواندن یک فایل را با مدیریت خطای مناسب (فایل پیدا نشد) بنویسید.
4. تابعی با annotation نوع بنویسید و با `mypy` بررسی کنید.

## مثال
```python
from typing import List

def total(items: List[int]) -> int:
    return sum(items)
```

> تایپینگ ایستا در Python اختیاری است، اما در کدهای تیمی و بزرگ اشتباهات را خیلی زودتر شکار می‌کند.

## اشتباهات رایج
- تغییر دادن لیستی که در حال پیمایش آن هستید (`for x in lst: lst.remove(x)`).
- استفاده از متغیرهای global که تست را سخت می‌کند.

## تمرین
یک ابزار CLI بسازید که یک پوشه را بخواند، تعداد خطوط هر فایل را بشمارد و خلاصه چاپ کند.''',
                "resources": "Python Docs — https://docs.python.org/3/tutorial, mypy — https://mypy.readthedocs.io, Real Python — https://realpython.com",
                "project": "ساخت یک ابزار CLI کوچک برای پردازش فایل‌ها.",
                "checkpoint": "ابزار با ورودی/خروجی صحیح و تست‌های واحد کار می‌کند.",
            },
            {
                "order": 2,
                "title": "ساختار داده‌ها و الگوریتم",
                "description": "بنیان حل مسئله و مصاحبه‌های فنی.",
                "content": '''## یادگیری در یک نگاه
درک ساختار داده‌ها کلید نوشتن کد کارا و تمیز است. انتخابِ اشتباهِ ساختار داده می‌تواند یک عملیات میلی‌ثانیه‌ای را به ثانیه‌ای تبدیل کند.

## مفاهیم کلیدی
- لیست، مجموعه (`set`)، دیکشنری و تاپل و زمان دسترسی هر کدام
- پیچیدگی زمانی و مکانی (نماد Big-O)
- پشته (stack)، صف (queue)، درخت و گراف در سطح مقدماتی
- الگوهای رایج: جستجو، مرتب‌سازی، دو اشاره‌گر (two pointers)
- تعادل بین خوانایی و بهینگی

## گام‌به‌گام
1. عملیات جستجو در لیست (O(n)) را با استفاده از `set` (O(1)) مقایسه کنید.
2. یک تابع بازگشتی برای فاکتوریل یا فیبوناچی بنویسید.
3. یک لیست را بدون تابع آماده مرتب‌سازی کنید (مثلاً merge sort).
4. پیچیدگی زمانی هر تابع را تحلیل کنید.

## مثال
```python
seen = set()
unique = [x for x in items if not (x in seen or seen.add(x))]
```

> همیشه اول راه‌حل درست را بنویسید، بعد بهینه‌سازی کنید؛ کد زودهنگام بهینه‌سازی‌شده معمولاً باگ‌دار است.

## اشتباهات رایج
- استفاده از لیست برای بررسی عضویت تکراری که کند است.
- نادیده گرفتن پیچیدگی در حلقه‌های تودرتو بزرگ.

## تمرین
یک ساختار دادهٔ سفارشی LRU cache پیاده‌سازی کنید با عملیات `get`/`put` در زمان ثابت.''',
                "resources": "VisuAlgo — https://visualgo.net, Big-O Cheat Sheet — https://www.bigocheatsheet.com, LeetCode — https://leetcode.com",
                "project": "پیاده‌سازی یک ساختار داده سفارشی (مثلاً LRU cache).",
                "checkpoint": "پیاده‌سازی در زمان مورد انتظار اجرا می‌شود.",
            },
            {
                "order": 3,
                "title": "پایگاه‌داده رابطه‌ای (SQL)",
                "description": "مدل‌سازی داده و کوئری‌های کارا.",
                "content": '''## یادگیری در یک نگاه
بیشتر اپلیکیشن‌ها روی یک پایگاه‌داده رابطه‌ای تکیه دارند. درک مدل‌سازی و کوئری‌های کارا تفاوت بین یک سرویس سریع و یک سرویس لنگ‌کننده است.

## مفاهیم کلیدی
- مدل‌سازی: جداول، کلید اصلی/خارجی و روابط ۱‑به‑چند و چند‑به‑چند
- کوئری‌های `SELECT`, `JOIN`, `GROUP BY`, `HAVING`
- ایندکس‌گذاری و تحلیل برنامهٔ اجرا با `EXPLAIN`
- تراکنش‌ها (transactions) و سطوح ایزولاسیون
- نرمال‌سازی در برابر denormalization برای خواندن سریع

## گام‌به‌گام
1. جداول `users`, `products`, `orders` را با کلیدهای خارجی طراحی کنید.
2. یک کوئری `JOIN` بنویسید که سفارش‌ها را با نام کاربر نشان دهد.
3. ایندکسی روی ستون پرتکرار بسازید و `EXPLAIN` را مقایسه کنید.
4. دو عملیات را در یک تراکنش قرار دهید.

## مثال
```sql
SELECT u.name, COUNT(o.id)
FROM users u
JOIN orders o ON o.user_id = u.id
GROUP BY u.name;
```

> ایندکس‌ها خواندن را سریع می‌کنند اما نوشتن را کندتر؛ پس ایندکس را فقط روی ستون‌های پرجستجو بسازید.

## اشتباهات رایج
- انجام joinهای سنگین در سمت اپلیکیشن به‌جای پایگاه‌داده.
- نادیده گرفتن تراکنش برای عملیات چندگانه مرتبط.

## تمرین
اسکیمای یک فروشگاه (محصول، سفارش، کاربر) در PostgreSQL طراحی کنید و کوئری اصلی را زیر ۱۰ms با ایندکس اجرا کنید.''',
                "resources": "PostgreSQL Tutorial — https://www.postgresqltutorial.com, Use The Index, Luke — https://use-the-index-luke.com, Mode SQL — https://mode.com/sql-tutorial",
                "project": "طراحی اسکیمای فروشگاهی (محصول، سفارش، کاربر) در PostgreSQL.",
                "checkpoint": "کوئری‌های اصلی با ایندکس مناسب زیر ۱۰ms اجرا می‌شوند.",
            },
            {
                "order": 4,
                "title": "طراحی REST API",
                "description": "قراردادهای ساخت endpointهای تمیز و قابل پیش‌بینی.",
                "content": '''## یادگیری در یک نگاه
یک API خوب قابل فهم، قابل تست و سازگار با نسخه‌های بعدی است. طراحی قراردادها قبل از پیاده‌سازی، درد بعدی را کم می‌کند.

## مفاهیم کلیدی
- منابع (resources) و افعال HTTP: `GET`, `POST`, `PUT`, `PATCH`, `DELETE`
- کدهای وضعیت معنادار: ۲۰۰, ۲۰۱, ۴۰۰, ۴۰۱, ۴۰۴, ۵۰۰
- نسخه‌بندی (`/v1/...`) و pagination
- مستندسازی با OpenAPI/Swagger
- idempotency و مدیریت یکپارچهٔ خطاها

## گام‌به‌گام
1. منابع را شناسایی کنید (مثلاً `/products`, `/orders`).
2. برای هر منبع افعال مناسب را تعیین کنید.
3. فرمت خطای یکپارچه (`{ "detail": "..." }`) تعریف کنید.
4. مستندات OpenAPI را برای endpointها تولید کنید.

## مثال
```http
GET    /v1/products?page=2&size=20
POST   /v1/products
GET    /v1/products/42
DELETE /v1/products/42
```

> فعل HTTP را برای عملیات انتخاب کنید، نه نام مسیر؛ `/deleteProduct` با متد GET ضدالگو است.

## اشتباهات رایج
- برگرداندن ۲۰۰ برای خطاهای کلاینت که ابزارها را گمراه می‌کند.
- تغییر شکل پاسخ بدون نسخه‌بندی که کلاینت‌های قدیمی را می‌شکند.

## تمرین
API یک انبار محصول با قراردادهای REST طراحی کنید و مستندات OpenAPI برای همه endpointها تولید کنید.''',
                "resources": "REST API Tutorial — https://restfulapi.net, OpenAPI — https://swagger.io/specification, HTTP Status Cats — https://http.cat",
                "project": "طراحی API یک انبار محصول با قراردادهای REST.",
                "checkpoint": "مستندات OpenAPI برای همه endpointها تولید می‌شود.",
            },
            {
                "order": 5,
                "title": "احراز هویت و امنیت",
                "description": "محافظت از endpointها و داده‌های کاربر.",
                "content": '''## یادگیری در یک نگاه
امنیت از ابتدا بخشی از طراحی است نه الحاقی به انتها. ضعف در احراز هویت یا ذخیرهٔ ناایمن رمز، رایج‌ترین راه نفوذ است.

## مفاهیم کلیدی
- احراز هویت با JWT و مفهوم refresh token
- هش کردن رمز عبور با `bcrypt` یا `argon2` (هیچ‌گاه متن ساده)
- کنترل دسترسی مبتنی بر نقش (RBAC)
- جلوگیری از حملات رایج: SQL injection, XSS, CSRF
- محدودیت نرخ (rate limiting) برای جلوگیری از حملهٔ brute force

## گام‌به‌گام
1. کاربر را ثبت‌نام کنید و رمز را با bcrypt هش کنید.
2. هنگام ورود توکن JWT صادر و در کلاینت ذخیره کنید.
3. یک dependency بنویسید که توکن را اعتبارسنجی و کاربر را تزریق کند.
4. endpointهای حساس را پشت آن dependency محافظت کنید.

## مثال
```python
from passlib.context import CryptContext
pwd = CryptContext(schemes=["bcrypt"])
hash = pwd.hash("secret123")
```

> توکن دسترسی (access token) را کوتاه‌عمر (مثلاً ۱۵ دقیقه) و refresh token را بلندعمر نگه دارید.

## اشتباهات رایج
- ذخیرهٔ رمز در متن ساده یا با هش ضعیف (MD5/SHA1 بدون نمک).
- قرار دادن توکن حساس در URL که در لاگ‌ها می‌ماند.

## تمرین
ثبت‌نام، ورود و محافظت از endpointهای کاربر را پیاده‌سازی کنید؛ توکن‌های منقضی‌شده رد شوند.''',
                "resources": "OWASP Top 10 — https://owasp.org/www-project-top-ten, Auth0 JWT — https://jwt.io/introduction, Passlib — https://passlib.readthedocs.io",
                "project": "افزودن ثبت‌نام، ورود و محافظت از endpointهای کاربر.",
                "checkpoint": "توکن‌های منقضی‌شده رد می‌شوند و رمز‌ها در متن ساده ذخیره نمی‌شوند.",
            },
            {
                "order": 6,
                "title": "فریم‌ورک وب (FastAPI)",
                "description": "ساخت API سریع با تایپینگ و اعتبارسنجی خودکار.",
                "content": '''## یادگیری در یک نگاه
FastAPI در کنار Pydantic تایپینگ و اعتبارسنجی را ساده می‌کند و به‌صورت خودکار مستندات تعاملی می‌سازد.

## مفاهیم کلیدی
- تعریف مسیرها با دکوراتور و تزریق وابستگی (`Depends`)
- مدل‌های Pydantic برای ورودی/خروجی و اعتبارسنجی خودکار
- یکپارچه‌سازی با SQLAlchemy (ORM) و مدیریت session
- میان‌افزارها (middleware) و تنظیم CORS
- مستندسازی خودکار با Swagger UI در `/docs`

## گام‌به‌گام
1. یک endpoint `GET /` بسازید که پیام JSON برمی‌گرداند.
2. یک مدل Pydantic برای ایجاد آیتم تعریف و اعتبارسنجی کنید.
3. اتصال به پایگاه‌داده با SQLAlchemy راه‌اندازی کنید.
4. یک dependency برای دریافت session پایگاه‌داده بنویسید.

## مثال
```python
@app.post("/items", response_model=ItemOut)
def create_item(data: ItemIn, db: Session = Depends(get_db)):
    return create(db, data)
```

> Pydantic هم ورودی را اعتبارسنجی می‌کند و هم شکل خروجی را تضمین می‌کند؛ این قراردادی مطمئن بین بک‌اند و فرانت‌اند می‌سازد.

## اشتباهات رایج
- برگرداندن مدل ORM مستقیماً که فیلدهای حساس (مثل هش رمز) لو می‌رود.
- باز کردن همهٔ منابع CORS در تولید.

## تمرین
یک API یادداشت‌ها بسازید با FastAPI + SQLAlchemy + SQLite و مستندات Swagger.''',
                "resources": "FastAPI — https://fastapi.tiangolo.com, SQLAlchemy — https://docs.sqlalchemy.org, Pydantic — https://docs.pydantic.dev",
                "project": "ساخت API یادداشت‌ها با FastAPI + SQLAlchemy + SQLite.",
                "checkpoint": "endpointها با تست‌های خودکار و مستندات Swagger کار می‌کنند.",
            },
            {
                "order": 7,
                "title": "کش و پیام‌رسانی (Redis / Queue)",
                "description": "مقیاس‌پذیری با کاهش بار پایگاه‌داده و پردازش غیرهمزمان.",
                "content": '''## یادگیری در یک نگاه
با رشد ترافیک، پاسخ‌های همزمان و پایگاه‌داده کش می‌آورند. کش و صف‌های پیام اجازه می‌دهند سیستم مقیاس‌پذیر بماند.

## مفاهیم کلیدی
- کش با Redis: `GET/SET`، زمان انقضا (TTL) و حذف هدفمند (invalidation)
- صف‌های پیام (Celery / RQ / RabbitMQ) برای کارهای سنگین
- پردازش غیرهمزمان وظایف (ایمیل، تولید گزارش)
- الگوی publisher/subscriber
- idempotent بودن پردازشگرهای صف

## گام‌به‌گام
1. یک مقدار را در Redis ذخیره و با TTL بخوانید.
2. نتیجهٔ یک کوئری پرتکرار را در کش قرار دهید.
3. یک وظیفهٔ پس‌زمینه (مثل ارسال ایمیل) با Celery/RQ تعریف کنید.
4. وظیفه را از داخل API به صف بفرستید.

## مثال
```python
cache.set("user:1", data, ex=300)  # ۵ دقیقه اعتبار
```

> کش را به‌عنوان «بهینه‌سازی» ببینید نه «منبع حقیقت»؛ همیشه راهی برای بازخوانی از منبع اصلی داشته باشید.

## اشتباهات رایج
- کش کردن داده‌های حساس یا خیلی ناپایدار.
- فراموش کردن بی‌اثر بودن (idempotency) پردازشگر صف که تکرار پیام را خراب می‌کند.

## تمرین
به API یادداشت‌ها کش نتایج جستجو و صف ارسال ایمیل اضافه کنید.''',
                "resources": "Redis — https://redis.io/docs, Celery — https://docs.celeryq.dev, RQ — https://python-rq.org",
                "project": "افزودن صف ایمیل و کش نتایج جستجو به API یادداشت‌ها.",
                "checkpoint": "ارسال ایمیل در پس‌زمینه انجام می‌شود و پاسخ API سریع می‌ماند.",
            },
            {
                "order": 8,
                "title": "تست، CI/CD و استقرار",
                "description": "اطمینان از کیفیت و تحویل خودکار.",
                "content": '''## یادگیری در یک نگاه
تحویل مداوم (CD) کیفیت را با خودکارسازی تضمین می‌کند. بدون تست و خط لوله، هر تغییر ریسکی بزرگ است.

## مفاهیم کلیدی
- تست واحد (pytest) و تست یکپارچه‌سازی (integration)
- پوشش کد (coverage) و تحلیل ایستا (linters)
- خط لوله CI با GitHub Actions
- کانتینری‌سازی با Docker
- استقرار روی PaaS/سرور ابری و rollback

## گام‌به‌گام
1. یک تست واحد برای یک تابع منطقی با pytest بنویسید.
2. پوشش کد را با `pytest --cov` اندازه‌گیری کنید.
3. یک فایل GitHub Actions بنویسید که روی هر push تست اجرا کند.
4. یک `Dockerfile` برای سرویس بنویسید و بسازید.

## مثال
```yaml
# .github/workflows/ci.yml
- run: pytest
```

> تست‌های کند را جدا کنید: تست‌های واحد سریع همیشه، تست‌های یکپارچه فقط در CI اجرا شوند.

## اشتباهات رایج
- تست‌هایی که به وضعیت جهانی وابسته‌اند و گاهی شکست می‌خورند (flakey).
- استقرار دستی که در لحظهٔ فشار کاری اشتباه می‌شود.

## تمرین
API را کانتینر کنید و خط لوله‌ای راه‌اندازی کنید که تست‌ها را اجرا و تصویر Docker بسازد.''',
                "resources": "pytest — https://docs.pytest.org, GitHub Actions — https://docs.github.com/actions, Docker — https://docs.docker.com/get-started",
                "project": "کانتینرسازی API و راه‌اندازی خط لوله CI که تست‌ها را اجرا می‌کند.",
                "checkpoint": "هر push تست‌ها را اجرا می‌کند و تصویر Docker ساخته می‌شود.",
            },
        ],
    },
    "devops": {
        "title": "مهندس DevOps",
        "subtitle": "از خط فرمان تا کانتینر، خط لوله و خوشه تولیدی",
        "description": "مسیر خودکارسازی، تحویل و پایداری سیستم‌های نرم‌افزاری.",
        "category": "devops",
        "color": "#10b981",
        "stages": [
            {
                "order": 1,
                "title": "Linux و Shell",
                "description": "زیربنای هر سرور و ابزار DevOps.",
                "content": '''## یادگیری در یک نگاه
تمرکز روی خط فرمان برای مدیریت سریع سیستم ضروری است؛ بیشتر ابزارهای DevOps در نهایت روی یک سرور Linux اجرا می‌شوند.

## مفاهیم کلیدی
- ساختار فایل‌سیستم استاندارد (FHS) و مسیرها
- مدیریت مجوزها (`chmod`, `chown`) و کاربران/گروه‌ها
- خط لوله (pipe `|`)، redirection (`>`, `>>`) و متغیرهای محیطی
- اسکریپت‌نویسی Bash برای خودکارسازی
- مدیریت فرآیندها با `systemd` و مشاهدهٔ لاگ با `journalctl`

## گام‌به‌گام
1. ساختار `/etc`, `/var`, `/home` را کاوش کنید.
2. یک فایل را با `chmod 600` ایمن کنید.
3. چند دستور را با pipe به هم وصل کنید (مثلاً `ps | grep`).
4. یک اسکریپت Bash برای پشتیبان‌گیری بنویسید.

## مثال
```bash
tar czf backup-$(date +%F).tgz /var/www
```

> اسکریپت‌ها را همیشه با `#!/usr/bin/env bash` و `set -euo pipefail` شروع کنید تا خطاها زود متوقف شوند.

## اشتباهات رایج
- اجرای دستورات به‌عنوان `root` بدون نیاز واقعی.
- فراموش کردن quote گذاری متغیرها که باعث شکستن روی نام‌های با فاصله می‌شود.

## تمرین
اسکریپتی بنویسید که هر شب از پایگاه‌داده پشتیبان بگیرد و قدیمی‌تر از ۷ روز را پاک کند.''',
                "resources": "Linux Journey — https://linuxjourney.com, Bash Guide — https://mywiki.wooledge.org/BashGuide, explainshell — https://explainshell.com",
                "project": "نوشتن یک اسکریپت پشتیبان‌گیری خودکار از پایگاه‌داده.",
                "checkpoint": "اسکریپت با cron به‌صورت زمان‌بندی‌شده اجرا می‌شود.",
            },
            {
                "order": 2,
                "title": "شبکه — مبانی",
                "description": "درک ارتباط بین سرویس‌ها و اینترنت.",
                "content": '''## یادگیری در یک نگاه
بیشتر مشکلات عملیاتی ریشه در شبکه دارند. درک لایه‌های شبکه کمک می‌کند سریع‌تر عیب‌یابی کنید.

## مفاهیم کلیدی
- مدل OSI و پروتکل‌های TCP/UDP
- آدرس‌دهی IP، زیرشبکه (subnet) و DNS
- پورت‌ها و فایروال‌ها (`ufw`, `iptables`)
- پروکسی و بار متوازن (load balancer)
- TLS/SSL و چرخهٔ گواهی‌ها

## گام‌به‌گام
1. با `ip addr` و `ping` اتصال را بررسی کنید.
2. یک نام دامنه را با `dig`/`nslookup` ردیابی کنید.
3. یک پورت را با فایروال باز کنید.
4. یک گواهی TLS با `openssl` بررسی کنید.

## مثال
```bash
curl -Iv https://example.com   # مشاهدهٔ دست‌بالا و گواهی
```

> وقتی چیزی کار نمی‌کند، لایه به لایه پیش بروید: فیزیکی → شبکه → انتقال → اپلیکیشن.

## اشتباهات رایج
- باز گذاشتن همهٔ پورت‌ها در فایروال برای «رفع سریع» مشکل.
- نادیده گرفتن انقضای گواهی TLS که باعث قطع ناگهانی می‌شود.

## تمرین
پیکربندی DNS و گواهی TLS برای یک دامنه آزمایشی طوری که با HTTPS بارگذاری شود.''',
                "resources": "Cloudflare Learning — https://www.cloudflare.com/learning, DigitalOcean Networking — https://www.digitalocean.com/community/tutorials, CURL man — https://curl.se/docs",
                "project": "پیکربندی DNS و گواهی TLS برای یک دامنه آزمایشی.",
                "checkpoint": "دامنه با HTTPS و بدون خطای گواهی بارگذاری می‌شود.",
            },
            {
                "order": 3,
                "title": "کنترل نسخه (Git)",
                "description": "همکاری ایمن روی کد منبع.",
                "content": '''## یادگیری در یک نگاه
Git استاندارد صنعت برای ردیابی تغییرات و همکاری تیمی است. درک مدل آن از «snapshot» به جای تفاوت‌ها کلید درک رفتارش است.

## مفاهیم کلیدی
- مفاهیم پایه: `commit`, `branch`, `merge`, `HEAD`
- workflowها: Gitflow یا trunk-based
- حل تداخل (conflict resolution) در فایل‌های متنی
- pull request و بازبینی کد (code review)
- بازنویسی تاریخچه با `rebase` (با احتیاط)

## گام‌به‌گام
1. یک مخزن بسازید و چند commit ثبت کنید.
2. یک شاخهٔ feature بسازید و تغییر را روی آن انجام دهید.
3. شاخه را به اصلی merge کنید (یا rebase کنید).
4. یک تداخل را به‌صورت دستی حل کنید.

## مثال
```bash
git switch -c feature/x
git commit -am "feat: add x"
git rebase main
```

> پیش از `push --force` همیشه فرض کنید همکارت روی همان شاخه کار می‌کند؛ force فقط روی شاخه‌های شخصی.

## اشتباهات رایج
- commit کردن فایل‌های حساس (کلیدها) که دیگر پاک کردنش سخت است.
- merge کردن بدون حل درست تداخل که باعث خرابی می‌شود.

## تمرین
یک مخزن با شاخه‌های feature راه‌اندازی کنید و یک تغییر را از طریق PR با بازبینی ادغام کنید.''',
                "resources": "Pro Git Book — https://git-scm.com/book, Learn Git Branching — https://learngitbranching.js.org, GitHub Flow — https://docs.github.com/en/get-started",
                "project": "راه‌اندازی یک مخزن با شاخه‌های feature و بررسی PR.",
                "checkpoint": "یک تغییر از طریق PR با بازبینی ادغام می‌شود.",
            },
            {
                "order": 4,
                "title": "کانتینرها (Docker)",
                "description": "بسته‌بندی اپلیکیشن و وابستگی‌هایش.",
                "content": '''## یادگیری در یک نگاه
کانتینرها محیط اجرا را یکسان و قابل حمل می‌کنند: «روی ماشین من کار می‌کرد» دیگر بهانه نیست.

## مفاهیم کلیدی
- تفاوت تصویر (image) در برابر کانتینر (container) در حال اجرا
- نوشتن `Dockerfile` بهینه (لایه‌ها و کش)
- حجم‌ها (volumes) برای دادهٔ پایدار و شبکه‌های داخلی
- `docker-compose` برای چند سرویس
- ثبت‌نام تصاویر (registry) و تگ‌گذاری

## گام‌به‌گام
1. یک `Dockerfile` ساده برای یک اپ Python/Node بنویسید.
2. تصویر را بسازید و کانتینر را اجرا کنید.
3. داده را با volume از کانتینر جدا کنید.
4. دو سرویس (اپ + پایگاه‌داده) را با compose بالا بیاورید.

## مثال
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]
```

> دستورات را از کم‌تغییرترین به پرتغییرترین مرتب کنید تا کش لایه‌ها بهتر استفاده شود.

## اشتباهات رایج
- کپی کردن کل پروژه شامل `.git` و `node_modules` که تصویر را غول‌پیکر می‌کند.
- ذخیرهٔ دادهٔ پایگاه‌داده در لایهٔ کانتینر (ناپایدار).

## تمرین
API یادداشت‌ها را داکرایز کنید به همراه PostgreSQL و با یک دستور بالا بیاورید.''',
                "resources": "Docker Docs — https://docs.docker.com/get-started, docker-compose — https://docs.docker.com/compose, Best practices — https://docs.docker.com/develop/dev-best-practices",
                "project": "داکرایز کردن API یادداشت‌ها به همراه PostgreSQL.",
                "checkpoint": "کل پشته با یک دستور `compose up` بالا می‌آید.",
            },
            {
                "order": 5,
                "title": "CI/CD",
                "description": "ساخت، تست و استقرار خودکار.",
                "content": '''## یادگیری در یک نگاه
خط لولهٔ تحویل خطای انسانی را کاهش می‌دهد. هدف: هر تغییر معتبر به‌سرعت و ایمن به تولید برسد.

## مفاهیم کلیدی
- مراحل: build → test → deploy
- مدیریت رازها (secrets) در خط لوله
- استقرار تدریجی (rolling / blue-green)
- قابلیت بازگشت (rollback) سریع
- quality gates (دروازه‌های کیفیت)

## گام‌به‌گام
1. روی هر push تست را اجرا کنید.
2. تصویر Docker را بسازید و در registry منتشر کنید.
3. استقرار را پشت یک تایید (manual approval) قرار دهید.
4. سناریوی بازگشت به نسخهٔ قبلی را تمرین کنید.

## مثال
```yaml
stages: [build, test, deploy]
deploy:
  when: manual
```

> هرگز رازها (توکن، کلید) را در فایل خط لوله کامیت نکنید؛ از متغیرهای محیطی امن استفاده کنید.

## اشتباهات رایج
- اجازه دادن به استقرار حتی وقتی تست شکست خورده (gate ضعیف).
- نداشتن نقشهٔ بازگشت که هنگام خرابی تولید بحران ایجاد می‌کند.

## تمرین
خط لوله‌ای بسازید که روی هر push تست اجرا و تصویر منتشر کند؛ شکست تست مانع استقرار شود.''',
                "resources": "GitHub Actions — https://docs.github.com/actions, GitLab CI — https://docs.gitlab.com/ee/ci, CI/CD concepts — https://www.redhat.com/en/topics/devops/what-is-ci-cd",
                "project": "خط لوله‌ای که روی هر push تست اجرا و تصویر منتشر می‌کند.",
                "checkpoint": "شکست تست مانع استقرار می‌شود.",
            },
            {
                "order": 6,
                "title": "زیرساخت به‌عنوان کد (Terraform)",
                "description": "تعریف زیرساخت به شکل قابل نسخه‌بندی.",
                "content": '''## یادگیری در یک نگاه
IaC زیرساخت را تکرارپذیر، قابل بازبینی و هم‌تراز با کد می‌کند؛ دیگر «روی کنسول ابری با دست» تنظیم نمی‌کنید.

## مفاهیم کلیدی
- منابع (resources) و providerها (AWS, GCP, Azure)
- فایل state و قفل‌های state از راه دور
- متغیرها (variables)، ماژول‌ها و خروجی‌ها (outputs)
- `plan`/`apply` و مدیریت تغییر
- جداسازی محیط‌های dev/staging/prod

## گام‌به‌گام
1. یک provider (مثلاً محلی با Docker) انتخاب کنید.
2. یک منبع ساده (مثلاً یک شبکه یا باکت) تعریف کنید.
3. `terraform plan` را ببینید و `apply` کنید.
4. منبع را تغییر دهید و plan دوباره بررسی کنید.

## مثال
```hcl
resource "aws_s3_bucket" "logs" {
  bucket = "my-app-logs"
}
```

> state را همیشه در یک مکان مشترک و قفل‌دار نگه دارید؛ state محلی در تیم باعث هم‌پوشانی و خرابی می‌شود.

## اشتباهات رایج
- کامیت کردن فایل state که حاوی اطلاعات حساس است.
- `apply` بدون `plan` که تغییرات غیرمنتظره را اعمال می‌کند.

## تمرین
یک سرور/باکت ابری ساده را با Terraform تعریف کنید و بازتولید کنید.''',
                "resources": "Terraform Docs — https://developer.hashicorp.com/terraform/docs, IaC — https://www.terraform.io/intro, AWS S3 — https://aws.amazon.com/s3",
                "project": "تعریف یک سرور ابری ساده با Terraform.",
                "checkpoint": "اجرای `apply` زیرساخت را بازتولید می‌کند.",
            },
            {
                "order": 7,
                "title": "هماهنگ‌سازی (Kubernetes)",
                "description": "مدیریت کانتینرها در مقیاس تولیدی.",
                "content": '''## یادگیری در یک نگاه
Kubernetes استقرار، مقیاس‌بندی و پایداری را خودکار می‌کند. درک مفاهیم پایهٔ آن پیش‌نیاز اجرای ایمن در تولید است.

## مفاهیم کلیدی
- `Pod` (واحد اجرا)، `Deployment` و `Service`
- `ConfigMap` و `Secret` برای پیکربندی
- بررسی‌های سلامت (liveness/readiness probes)
- مقیاس‌بندی خودکار (HPA)
- `Ingress` برای مسیریابی ترافیک

## گام‌به‌گام
1. یک Deployment ساده با چند replica بسازید.
2. یک Service از نوع ClusterIP تعریف کنید.
3. probeهای سلامت به کانتینر اضافه کنید.
4. ترافیک را با Ingress مسیریابی کنید.

## مثال
```yaml
apiVersion: apps/v1
kind: Deployment
spec:
  replicas: 3
```

> liveness probe تعیین می‌کند کی کانتینر ری‌استارت شود؛ readiness probe تعیین می‌کند کی ترافیک دریافت کند.

## اشتباهات رایج
- قرار دادن رازها در ConfigMap به‌جای Secret.
- نداشتن resource limits که یک Pod کل گره را اشغال کند.

## تمرین
اپ را روی Minikube با سرویس و Ingress مستقر کنید.''',
                "resources": "Kubernetes Docs — https://kubernetes.io/docs/tutorials, Concepts — https://kubernetes.io/docs/concepts, K8s by examples — https://kubernetesbyexample.com",
                "project": "استقرار اپ روی Minikube با سرویس و Ingress.",
                "checkpoint": "اپ با ترافیک واقعی مقیاس‌بندی و بازیافت می‌شود.",
            },
            {
                "order": 8,
                "title": "مشاهده‌پذیری (Monitoring)",
                "description": "دید به سلامت و عملکرد سیستم.",
                "content": '''## یادگیری در یک نگاه
بدون مشاهده‌پذیری، عیب‌یابی در تولید غیرممکن است. سه ستون آن logs و metrics و traces هستند.

## مفاهیم کلیدی
- سه ستون: logs, metrics, traces
- جمع‌آوری متریک با Prometheus
- داشبورد با Grafana
- هشدارها (alerting) و تعریف SLO/SLI
- توزیع حلقه‌های دیباگ (distributed tracing)

## گام‌به‌گام
1. یک متریک سفارشی (مثلاً زمان پاسخ) از اپ expose کنید.
2. Prometheus را برای خزش (scrape) آن تنظیم کنید.
3. یک داشبورد Grafana بسازید.
4. یک قانون هشدار روی افزایش زمان پاسخ تعریف کنید.

## مثال
```yaml
scrape_configs:
  - job_name: app
    static_configs: [{ targets: ["app:8000"] }]
```

> SLO را بر اساس تجربهٔ کاربر تعریف کنید نه بر اساس آنچه اندازه‌گیری آسان است.

## اشتباهات رایج
- هشدارهای زیاد و بی‌اهمیت که باعث «خستگی هشدار» می‌شود.
- نگاه کردن فقط به لاگ‌ها و نادیده گرفتن متریک‌های کلان.

## تمرین
متریک و داشبورد سلامت برای اپ اضافه کنید و هشدار روی افزایش زمان پاسخ فعال کنید.''',
                "resources": "Prometheus — https://prometheus.io/docs, Grafana — https://grafana.com/docs, Google SRE Book — https://sre.google/sre-book",
                "project": "افزودن متریک و داشبورد سلامت برای اپ.",
                "checkpoint": "هشدار روی افزایش زمان پاسخ‌دهی به‌درستی عمل می‌کند.",
            },
        ],
    },
    "mobile": {
        "title": "توسعه‌دهنده Mobile",
        "subtitle": "از مفاهیم موبایل تا انتشار اپ روی iOS و Android",
        "description": "مسیر ساخت اپلیکیشن‌های موبایل با React Native: کامپوننت، ناوبری، دستگاه و انتشار.",
        "category": "mobile",
        "color": "#f97316",
        "stages": [
            {
                "order": 1,
                "title": "مبانی توسعه موبایل",
                "description": "تفاوت پلتفرم‌ها و انتخاب رویکرد.",
                "content": '''## یادگیری در یک نگاه
قبل از کد زدن باید بدانید native، hybrid و cross-platform چه تفاوتی دارند و کدام برای هدف شما مناسب‌تر است.

## مفاهیم کلیدی
- تفاوت native (Swift/Kotlin)، hybrid (WebView) و cross-platform (Flutter/React Native)
- چرخهٔ عمر اپ (lifecycle) و مفهوم «صفحه» (screen) در برابر «وب‌سایت»
- ابزارهای تست روی شبیه‌ساز (emulator/simulator) و دستگاه واقعی
- محدودیت‌های موبایل: باتری، شبکه ناپایدار و صفحه کوچک

## گام‌به‌گام
1. یک شبیه‌ساز Android/iOS راه‌اندازی کنید.
2. یک پروژهٔ خالی React Native (یا Expo) بسازید.
3. پروژه را روی شبیه‌ساز اجرا کنید.
4. تفاوت اجرا روی دستگاه واقعی را بررسی کنید.

## مثال
```bash
npx create-expo-app@latest MyApp
cd MyApp && npx expo start
```

> شروع با Expo سریع‌ترین مسیر برای یادگیری است؛ کد native سفارشی بعداً با `expo prebuild` ممکن می‌شود.

## اشتباهات رایج
- تلاش برای بازسازی دقیق رابط وب روی موبایل که با انتظارات کاربر فاصله دارد.
- نادیده گرفتن تست روی دستگاه واقعی.

## تمرین
یک پروژهٔ خالی بسازید و «سلام دنیا» را روی شبیه‌ساز اجرا کنید.''',
                "resources": "React Native — https://reactnative.dev/docs/getting-started, Expo — https://docs.expo.dev, Flutter — https://docs.flutter.dev",
                "project": "راه‌اندازی پروژه خالی و اجرا روی شبیه‌ساز.",
                "checkpoint": "پروژه روی شبیه‌ساز/دستگاه اجرا می‌شود.",
            },
            {
                "order": 2,
                "title": "کامپوننت‌ها و چیدمان",
                "description": "ساخت رابط با کامپوننت‌های بومی و Flexbox.",
                "content": '''## یادگیری در یک نگاه
در React Native بسیاری از عناصر HTML با معادل بومی جایگزین می‌شوند (`View` به‌جای `div`، `Text` به‌جای `p`). چیدمان همچنان با Flexbox است.

## مفاهیم کلیدی
- کامپوننت‌های اصلی: `View`, `Text`, `Image`, `ScrollView`, `Pressable`
- چیدمان با Flexbox (در موبایل پیش‌فرض `flexDirection: column`)
- واحدهای پیکسل مستقل (`dp`) و `Dimensions`
- استایل‌دهی با شیء StyleSheet
- پاسخ‌گویی به اندازهٔ صفحهٔ دستگاه

## گام‌به‌گام
1. یک صفحه با `View` و `Text` بسازید.
2. یک لیست را با `ScrollView` نمایش دهید.
3. چیدمان را با Flexbox (center, space-between) تنظیم کنید.
4. دکمه‌ای با `Pressable` و مدیریت کلیک بسازید.

## مثال
```tsx
<View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
  <Text>خوش آمدید</Text>
</View>
```

> همیشه متن را داخل کامپوننت `Text` قرار دهید؛ رشتهٔ خام مستقیم در `View` در RN کار نمی‌کند.

## اشتباهات رایج
- فراموش کردن `flex: 1` که باعث می‌شود چیدمان فضای عمودی نگیرد.
- استفاده از عرض/ارتفاع ثابت پیکسل به‌جای نسبی.

## تمرین
یک صفحهٔ پروفایل موبایل با آواتار، نام و لیست مهارت‌ها بسازید.''',
                "resources": "RN Layout — https://reactnative.dev/docs/flexbox, RN Components — https://reactnative.dev/docs/components-and-apis, StyleSheet — https://reactnative.dev/docs/stylesheet",
                "project": "ساخت صفحه پروفایل با View/Text/Image.",
                "checkpoint": "رابط روی اندازه‌های مختلف صفحه تمیز است.",
            },
            {
                "order": 3,
                "title": "ناوبری (Navigation)",
                "description": "جابه‌جایی بین صفحه‌ها با React Navigation.",
                "content": '''## یادگیری در یک نگاه
اپلیکیشن‌های موبایل چند صفحه دارند. کتابخانهٔ React Navigation استاندارد جابه‌جایی بین آن‌هاست.

## مفاهیم کلیدی
- انواع ناوبری: Stack، Tab، Drawer
- ارسال پارامتر بین صفحه‌ها (`route.params`)
- هدر و دکمهٔ بازگشت
- deep linking و مسیرهای وب
- مدیریت وضعیت ناوبری

## گام‌به‌گام
1. یک `NavigationContainer` با یک Stack بسازید.
2. دو صفحهٔ Home و Detail تعریف کنید.
3. از Home به Detail با پارامتر بروید.
4. یک Tab Navigator با سه تب اضافه کنید.

## مثال
```tsx
<Stack.Screen name="Detail" component={Detail} />
navigation.navigate('Detail', { id: 1 })
```

> ناوبری را در لایهٔ بالا نگه دارید؛ منطق صفحه نباید نام صفحهٔ بعدی را بشناسد.

## اشتباهات رایج
- ناوبری مستقیم داخل کامپوننت‌های عمیق که اقتران (coupling) ایجاد می‌کند.
- فراموش کردن کلید یکتا برای لیست آیتم‌های ناوبری.

## تمرین
اپی با سه صفحه (لیست، جزئیات، تنظیمات) و انتقال پارامتردار بسازید.''',
                "resources": "React Navigation — https://reactnavigation.org/docs/getting-started, Stack — https://reactnavigation.org/docs/stack-navigator, Tabs — https://reactnavigation.org/docs/bottom-tab-navigator",
                "project": "ساخت ناوبری Stack/Tab بین چند صفحه.",
                "checkpoint": "جابه‌جایی بین صفحه‌ها با پارامتر کار می‌کند.",
            },
            {
                "order": 4,
                "title": "مدیریت وضعیت",
                "description": "وضعیت محلی و سراسری در اپ موبایل.",
                "content": '''## یادگیری در یک نگاه
مانند وب، وضعیت در موبایل هم محلی (یک صفحه) و هم سراسری (کاربر وارد شده) دارد. انتخاب ابزار مناسب کلید است.

## مفاهیم کلیدی
- `useState` برای وضعیت محلی صفحه
- Context برای داده‌های سبک سراسری
- Zustand یا Redux Toolkit برای سناریوهای پیچیده
- ذخیرهٔ پایدار با AsyncStorage / MMKV
- بازیابی وضعیت هنگام باز شدن دوبارهٔ اپ

## گام‌به‌گام
1. وضعیت یک فرم را با `useState` مدیریت کنید.
2. وضعیت کاربر را در یک Context قرار دهید.
3. یک مقدار را در AsyncStorage ذخیره و بخوانید.
4. اپ را ببندید و باز کنید تا داده باقی بماند.

## مثال
```tsx
const [name, setName] = useState('')
```

> وضعیت سراسری را فقط برای داده‌هایی که واقعاً مشترک‌اند نگه دارید؛ بقیه را محلی نگه دارید تا رندر بهینه بماند.

## اشتباهات رایج
- ذخیرهٔ حجم زیاد در AsyncStorage که راه‌اندازی را کند می‌کند.
- ری‌رندر کل درخت به‌خاطر یک تغییر کوچک.

## تمرین
اپی بسازید که نام کاربر را ذخیره و هنگام باز شدن دوبارهٔ اپ بخواند.''',
                "resources": "Zustand — https://github.com/pmndrs/zustand, AsyncStorage — https://react-native-async-storage.github.io/async-storage, Redux Toolkit — https://redux-toolkit.js.org",
                "project": "مدیریت وضعیت با Context + ذخیره پایدار.",
                "checkpoint": "داده پس از بستن و باز کردن اپ باقی می‌ماند.",
            },
            {
                "order": 5,
                "title": "دسترسی به دستگاه",
                "description": "دوربین، حافظه، موقعیت و سنسورها.",
                "content": '''## یادگیری در یک نگاه
مزیت موبایل دسترسی به سخت‌افزار دستگاه است. کتابخانه‌هایی مثل Expo APIs این دسترسی‌ها را یکپارچه می‌کنند.

## مفاهیم کلیدی
- درخواست اجازه (permissions) در زمان اجرا
- دوربین و گالری (`expo-image-picker`)
- حافظهٔ فایل (`expo-file-system`)
- موقعیت مکانی (Location)
- اعلان‌ها (Notifications)

## گام‌به‌گام
1. اجازهٔ دوربین را درخواست کنید.
2. عکس بگیرید و پیش‌نمایش دهید.
3. عکس را در حافظهٔ دستگاه ذخیره کنید.
4. یک اعلان محلی نمایش دهید.

## مثال
```tsx
const res = await ImagePicker.launchCameraAsync()
```

> همیشه درخواست اجازه را در زمان نیاز بدهید نه در شروع اپ؛ کاربر رد کردن اجازه در بدو ورود را ترجیح می‌دهد.

## اشتباهات رایج
- فراموش کردن اعلام اجازه در فایل تنظیمات پلتفرم (Android/iOS).
- فرض گرفتن همیشه در دسترس بودن سنسور.

## تمرین
اپی بسازید که عکس بگیرد، ذخیره کند و در گالری نشان دهد.''',
                "resources": "Expo ImagePicker — https://docs.expo.dev/versions/latest/sdk/image-picker, Expo Location — https://docs.expo.dev/versions/latest/sdk/location, Permissions — https://docs.expo.dev/guides/permissions",
                "project": "دسترسی به دوربین و ذخیرهٔ تصویر.",
                "checkpoint": "گرفتن عکس، ذخیره و نمایش در گالری کار می‌کند.",
            },
            {
                "order": 6,
                "title": "شبکه و API",
                "description": "دریافت و ارسال داده از سرور.",
                "content": '''## یادگیری در یک نگاه
اپلیکیشن موبایل معمولاً داده را از یک API می‌گیرد. مدیریت شبکه ناپایدار بخش مهم تجربهٔ کاربر است.

## مفاهیم کلیدی
- فراخوانی REST با `fetch` یا کتابخانه‌هایی مثل TanStack Query
- وضعیت‌های loading / error / empty
- کش و همگام‌سازی آفلاین
- احراز هویت با توکن در هدر درخواست
- فرمت‌های تصویر و بهینه‌سازی حجم

## گام‌به‌گام
1. داده‌ای را با `fetch` از یک API بگیرید.
2. وضعیت loading و error را در رابط نشان دهید.
3. درخواست‌ها را با TanStack Query کش کنید.
4. توکن احراز هویت را در هدر بفرستید.

## مثال
```tsx
const { data, isLoading } = useQuery({
  queryKey: ['posts'],
  queryFn: () => fetch('/api/posts').then(r => r.json()),
})
```

> در موبایل شبکه همیشه پایدار نیست؛ همیشه حالت آفلاین و تلاش مجدد (retry) را در نظر بگیرید.

## اشتباهات رایج
- نادیده گرفتن وضعیت خطا که باعث صفحهٔ سفید می‌شود.
- درخواست سنگین روی هر رندر که باتری و دیتا را هدر می‌دهد.

## تمرین
لیستی از پست‌ها را از API بگیرید و با مدیریت خطا/بارگذاری نمایش دهید.''',
                "resources": "TanStack Query RN — https://tanstack.com/query/latest, Fetch API — https://developer.mozilla.org/ru/docs/Web/API/Fetch_API, RN Networking — https://reactnative.dev/docs/network",
                "project": "دریافت لیست از API با مدیریت خطا/بارگذاری.",
                "checkpoint": "لیست با وضعیت بارگذاری/خطا به‌درستی نمایش داده می‌شود.",
            },
            {
                "order": 7,
                "title": "انتشار (iOS / Android)",
                "description": "بسته‌بندی و انتشار روی فروشگاه‌ها.",
                "content": '''## یادگیری در یک نگاه
رساندن اپ به دست کاربر یعنی بسته‌بندی و انتشار روی App Store و Google Play. هر پلتفرم فرآیند و مقررات خودش را دارد.

## مفاهیم کلیدی
- ساخت نسخهٔ release (APK/AAB برای Android، IPA برای iOS)
- امضای اپلیکیشن (signing) و شناسهٔ بسته
- حساب توسعه‌دهنده (Apple Developer / Google Play Console)
- بررسی (review) و خطاهای رایج رد شدن
- به‌روزرسانی تدریجی (staged rollout)

## گام‌به‌گام
1. یک نسخهٔ release با Expo/EAS یا Android Studio بسازید.
2. آیکون و برچسب‌های محیطی (splash) را تنظیم کنید.
3. باندل را در کنسول آپلود کنید.
4. لیست فروشگاه (توضیحات، تصاویر) را کامل کنید.

## مثال
```bash
eas build --platform android --profile production
```

> پیش از ارسال، راهنمای بررسی اپل را بخوانید؛ بیشتر رد شدن‌ها به‌خاطر نقض سادهٔ خطوط راهنما است.

## اشتباهات رایج
- نسخهٔ debug را با امضای نادرست فرستادن.
- نادیده گرفتن حریم خصوصی (سیاست حریم) که باعث رد می‌شود.

## تمرین
بیلد نسخهٔ انتشار را بسازید و در کنسول آپلود کنید (حتی اگر منتشر نکنید).''',
                "resources": "Expo EAS Build — https://docs.expo.dev/build/introduction, Android Publish — https://developer.android.com/studio/publish, App Store — https://developer.apple.com/app-store/review",
                "project": "ساخت بیلد انتشار و آپلود در کنسول.",
                "checkpoint": "بیلد انتشار بدون خطای امضا ساخته می‌شود.",
            },
            {
                "order": 8,
                "title": "عملکرد و تست",
                "description": "سریع نگه‌داشتن اپ و اطمینان از کیفیت.",
                "content": '''## یادگیری در یک نگاه
عملکرد و پایداری در موبایل حیاتی‌اند: کاربر اپی که لگد می‌زند را سریع حذف می‌کند.

## مفاهیم کلیدی
- جلوگیری از ری‌رندرهای بی‌دلیل (memo, useCallback)
- لیست‌های بزرگ با `FlatList` به‌جای `ScrollView`
- تست واحد (Jest) و تست کامپوننت (React Native Testing Library)
- کاهش حجم باندل و تصاویر
- ابزارهای پروفایل (Flipper / Android Studio Profiler)

## گام‌به‌گام
1. یک لیست بزرگ را با `FlatList` نمایش دهید.
2. یک تست واحد برای یک تابع منطقی بنویسید.
3. کامپوننتی را با Testing Library رندر و تأیید کنید.
4. ری‌رندرهای اضافی را با `memo` کاهش دهید.

## مثال
```tsx
<FlatList data={items} renderItem={renderItem} keyExtractor={i => i.id} />
```

> برای لیست‌های طولانی همیشه `FlatList` استفاده کنید؛ `ScrollView` همهٔ آیتم‌ها را یکجا رندر می‌کند.

## اشتباهات رایع
- رندر هزاران آیتم با ScrollView که حافظه را پر می‌کند.
- نادیده گرفتن تست که باعث خرابی در نسخهٔ بعدی می‌شود.

## تمرین
اپ را با FlatList و تست‌های پایه تجهیز کنید و نمرهٔ عملکرد را در پروفایلر بررسی کنید.''',
                "resources": "RN Performance — https://reactnative.dev/docs/performance, Jest — https://jestjs.io, RN Testing Library — https://callstack.github.io/react-native-testing-library",
                "project": "بهینه‌سازی لیست با FlatList + تست پایه.",
                "checkpoint": "لیست بزرگ بدون افت حافظه اسکرول می‌کند.",
            },
        ],
    },
}


# ---------------------------------------------------------------------------
# Course definitions — each lesson carries complete, actionable content.
# ---------------------------------------------------------------------------

COURSES: dict[str, dict] = {
    "fastapi": {
        "title": "دوره عملی FastAPI",
        "description": "ساخت یک REST API کامل با FastAPI، SQLAlchemy و احراز هویت JWT — از صفر تا اجرا.",
        "category": "backend",
        "level": "beginner",
        "instructor_name": "تیم DevHub",
        "is_free": True,
        "duration_hours": 6,
        "lessons": [
            {
                "order": 1,
                "title": "راه‌اندازی پروژه",
                "content": '''## هدف این درس
یک پروژهٔ FastAPI حداقل بسازید که روی آدرس `/` یک پاسخ JSON برگرداند و مستندات تعاملی داشته باشد.

## گام‌به‌گام
1. یک محیط مجازی بسازید و فعال کنید.
2. بسته‌ها را نصب کنید: `fastapi` و `uvicorn[standard]`.
3. فایل `main.py` با یک endpoint سلام بنویسید.
4. سرور را با `uvicorn main:app --reload` اجرا کنید.

## مثال
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "سلام از DevHub API"}
```

## بررسی
- مسیر `/` پیام JSON برمی‌گرداند.
- مستندات در `/docs` (Swagger UI) در دسترس است.

> پرچم `--reload` فقط در توسعه استفاده شود؛ در تولید سرور را بدون آن اجرا کنید.

## تمرین
یک endpoint `/health` اضافه کنید که `{"status": "ok"}` برگرداند.''',
                "video_url": None,
                "duration_minutes": 20,
            },
            {
                "order": 2,
                "title": "مدل‌ها و Schemaها",
                "content": '''## هدف این درس
تفکیک لایهٔ پایگاه‌داده (ORM) از لایهٔ قرارداد API (Pydantic) را یاد بگیرید.

## مفاهیم
- `Base` مشترک برای همه مدل‌های SQLAlchemy
- ستون‌ها با `Column` و انواع (`Integer`, `String`)
- مدل‌های Pydantic برای ورودی (`...In`) و خروجی (`...Out`)
- جداسازی این دو لایه برای خوانایی و امنیت

## مثال
```python
class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True)
    title = Column(String(120))

class ItemOut(BaseModel):
    id: int
    title: str
```

> هرگز مدل ORM را مستقیماً به کلاینت برنگردانید؛ همیشه از یک schema خروجی استفاده کنید تا فیلدهای حساس لو نروند.

## اشتباهات رایج
- برگرداندن رکورد ORM که فیلدهای داخلی را فاش می‌کند.
- تعریف تکراری ستون‌ها در هر دو لایه.

## تمرین
مدل `Item` و schemaهای `ItemIn`/`ItemOut` را بنویسید.''',
                "video_url": None,
                "duration_minutes": 40,
            },
            {
                "order": 3,
                "title": "مسیرها و اعتبارسنجی",
                "content": '''## هدف این درس
endpointهای CRUD بنویسید و ورودی را با تایپ پایتون اعتبارسنجی کنید.

## گام‌به‌گام
1. `GET /items` با لیست و pagination.
2. `POST /items` برای ایجاد با بدنهٔ معتبر.
3. `GET /items/{id}` با مدیریت «پیدا نشد».
4. تزریق session پایگاه‌داده با `Depends`.

## مثال
```python
@app.post("/items", response_model=ItemOut, status_code=201)
def create(data: ItemIn, db: Session = Depends(get_db)):
    item = Item(**data.model_dump())
    db.add(item); db.commit(); db.refresh(item)
    return item
```

> کد وضعیت ۲۰۱ فقط برای ایجاد منبع استفاده شود؛ بقیه عملیات معمولاً ۲۰۰ برمی‌گردانند.

## اشتباهات رایج
- برگرداندن ۲۰۰ برای منبع تازه ایجاد شده.
- نادیده گرفتن حالت «پیدا نشد» که ۵۰۰ برمی‌گرداند.

## تمرین
عملیات به‌روزرسانی و حذف را هم اضافه کنید.''',
                "video_url": None,
                "duration_minutes": 45,
            },
            {
                "order": 4,
                "title": "احراز هویت با JWT",
                "content": '''## هدف این درس
ثبت‌نام، ورود و محافظت از مسیرهای خصوصی با توکن JWT.

## گام‌به‌گام
1. رمز عبور را با `bcrypt` هش کنید.
2. هنگام ورود توکن JWT صادر کنید.
3. تابع `get_current_user` را با `Depends` بنویسید.
4. مسیرهای خصوصی را پشت آن محافظت کنید.

## مثال
```python
token = create_access_token({"sub": str(user.id)})
```

> کلید امضا (secret key) را از متغیر محیطی بخوانید، هرگز در کد ننویسید.

## اشتباهات رایج
- ذخیرهٔ رمز در متن ساده.
- انقضای بسیار طولانی توکن دسترسی.

## تمرین
یک مسیر `/me` بسازید که فقط با توکن معتبر پاسخ دهد.''',
                "video_url": None,
                "duration_minutes": 50,
            },
            {
                "order": 5,
                "title": "تست و مستندسازی",
                "content": '''## هدف این درس
تست‌های یکپارچه با `httpx` و `pytest` بنویسید و خروجی OpenAPI را بررسی کنید.

## گام‌به‌گام
1. یک کلاینت تست ASGI راه‌اندازی کنید.
2. تست برای ایجاد و خواندن آیتم بنویسید.
3. کدهای وضعیت را تأیید کنید.
4. مستندات OpenAPI را از `app.openapi()` بخوانید.

## مثال
```python
def test_create(client):
    res = client.post("/items", json={"title": "x"})
    assert res.status_code == 201
```

> تست‌ها را ایزوله نگه دارید: هر تست باید روی پایگاه‌دادهٔ تست اجرا شود نه تولید.

## اشتباهات رایج
- وابسته کردن تست‌ها به ترتیب اجرا.
- تست روی پایگاه‌دادهٔ واقعی.

## تمرین
پوشش تست حداقل برای endpointهای اصلی را بنویسید.''',
                "video_url": None,
                "duration_minutes": 35,
            },
        ],
    },
    "react": {
        "title": "دوره React از صفر",
        "description": "ساخت رابط‌های کاربری تعاملی با React و TypeScript — مفاهیم پایه تا مدیریت وضعیت.",
        "category": "frontend",
        "level": "beginner",
        "instructor_name": "تیم DevHub",
        "is_free": True,
        "duration_hours": 5,
        "lessons": [
            {
                "order": 1,
                "title": "کامپوننت اول",
                "content": '''## هدف این درس
درک اینکه کامپوننت تابعی است که JSX برمی‌گرداند و چگونه `props` و `state` کار می‌کنند.

## گام‌به‌گام
1. پروژه را با Vite و قالب React راه‌اندازی کنید.
2. یک کامپوننت `Counter` با `useState` بسازید.
3. مقدار را با دکمه افزایش دهید.
4. مقدار را در رابط نشان دهید.

## مثال
```tsx
function Counter() {
  const [count, setCount] = useState(0)
  return <button onClick={() => setCount(count + 1)}>{count}</button>
}
```

> هرگز state را مستقیماً تغییر ندهید (`count++`)؛ همیشه نسخهٔ جدید با setter بسازید.

## اشتباهات رایج
- تغییر مستقیم state که باعث عدم رندر می‌شود.
- استفاده از index به‌عنوان `key`.

## تمرین
یک شمارنده که هم افزایش و هم کاهش دارد بسازید.''',
                "video_url": None,
                "duration_minutes": 25,
            },
            {
                "order": 2,
                "title": "رویدادها و فرم‌ها",
                "content": '''## هدف این درس
مدیریت رویدادهای کاربر و کنترل فرم‌ها با controlled input.

## گام‌به‌گام
1. مقدار input را در state نگه دارید.
2. با `onChange` مقدار را به‌روز کنید.
3. با `onSubmit` از رفتار پیش‌فرض مرورگر جلوگیری کنید.
4. ورودی را پیش از ارسال اعتبارسنجی کنید.

## مثال
```tsx
<form onSubmit={(e) => { e.preventDefault(); alert(name) }}>
  <input value={name} onChange={(e) => setName(e.target.value)} />
</form>
```

> فرم‌های بزرگ را با یک کتابخانه (مثل React Hook Form) مدیریت کنید تا ری‌رندر کمتر شود.

## اشتباهات رایج
- فراموش کردن `e.preventDefault()` که صفحه ری‌لود می‌شود.
- خواندن state بلافاصیل بعد از `setName` (هنوز به‌روزرسانی نشده).

## تمرین
فرم ثبت‌نام ساده با نام و ایمیل و اعتبارسنجی بسازید.''',
                "video_url": None,
                "duration_minutes": 30,
            },
            {
                "order": 3,
                "title": "اثرهای جانبی (useEffect)",
                "content": '''## هدف این درس
اجرای اثرهای جانبی مثل فراخوانی API با `useEffect` و مدیریت وابستگی‌ها.

## گام‌به‌گام
1. داده را در `useEffect` با آرایهٔ وابستگی خالی بگیرید.
2. وضعیت‌های loading و error را مدیریت کنید.
3. درخواست را هنگام unmount لغو (cleanup) کنید.
4. وابستگی‌ها را درست تنظیم کنید تا حلقه ایجاد نشود.

## مثال
```tsx
useEffect(() => {
  const ctrl = new AbortController()
  fetch(url, { signal: ctrl.signal }).then(r => r.json())
  return () => ctrl.abort()
}, [url])
```

> آرایهٔ وابستگی اشتباه رایج‌ترین علت حلقه‌های بی‌پایان و درخواست‌های تکراری است.

## اشتباهات رایج
- آرایهٔ وابستگی را رها کردن که اثر هر بار اجرا می‌شود.
- نادیده گرفتن لغو درخواست (نشت حافظه).

## تمرین
داده‌ای از یک API بگیرید و با مدیریت خطا نمایش دهید.''',
                "video_url": None,
                "duration_minutes": 35,
            },
            {
                "order": 4,
                "title": "مدیریت وضعیت",
                "content": '''## هدف این درس
با بزرگ‌شدن اپ، وضعیت را از کامپوننت‌ها خارج کنید و بین بخش‌های مشترک همگام کنید.

## گام‌به‌گام
1. داده‌های سراسری سبک را با Context به اشتراک بگذارید.
2. سناریوهای پیچیده را با Zustand مدیریت کنید.
3. انتخاب‌گرهای دقیق بنویسید تا ری‌رندر کم شود.
4. وضعیت را از localStorage بازیابی کنید.

## مثال
```tsx
const useStore = create((set) => ({ count: 0, inc: () => set(s => ({ count: s.count + 1 })) }))
```

> همهٔ state را سراسری نکنید؛ فقط آنچه واقعاً مشترک است.

## اشتباهات رایج
- قرار دادن state محلی در store سراسری.
- ری‌رندر کل درخت به‌خاطر یک تغییر کوچک.

## تمرین
یک سبد خرید کوچک با Zustand و ذخیرهٔ پایدار بسازید.''',
                "video_url": None,
                "duration_minutes": 40,
            },
        ],
    },
}


def seed_demo_data() -> None:
    """Idempotently insert demo rows when the database is empty."""
    db = SessionLocal()
    try:
        if db.scalar(select(User).limit(1)):
            return

        # Users
        dev = User(
            email="demo@devhub.app",
            full_name="سارا محمدی",
            password_hash=hash_password("demo12345"),
            role="developer",
            bio="توسعه‌دهنده Frontend با تمرکز بر React و TypeScript.",
            is_verified=True,
        )
        employer = User(
            email="employer@devhub.app",
            full_name="Nova Fintech",
            password_hash=hash_password("demo12345"),
            role="employer",
            is_employer=True,
            company="Nova Fintech",
        )
        admin = User(
            email="admin@devhub.app",
            full_name="DevHub Admin",
            password_hash=hash_password("demo12345"),
            role="admin",
            is_verified=True,
        )
        db.add_all([dev, employer, admin])
        db.flush()

        db.add_all(
            [
                Skill(user_id=dev.id, name="React", level="intermediate"),
                Skill(user_id=dev.id, name="TypeScript", level="intermediate"),
                Skill(user_id=dev.id, name="Python", level="beginner"),
                Skill(user_id=employer.id, name="DevOps", level="expert"),
            ]
        )

        # Jobs
        job1 = Job(
            owner_id=employer.id,
            title="Frontend Developer (React / TypeScript)",
            company="Nova Fintech",
            description="ساخت و نگهداری اپلیکیشن‌های مدرن React با تمرکز بر عملکرد و تجربه کاربری.",
            location="تهران / دورکاری",
            type="full_time",
            mode="remote",
            level="mid",
            salary_range="۳۰,۰۰۰,۰۰۰ - ۵۰,۰۰۰,۰۰۰ تومان",
            skills="React,TypeScript,Next.js",
            is_featured=True,
            budget=200000,
        )
        job2 = Job(
            owner_id=employer.id,
            title="Backend Engineer (FastAPI / PostgreSQL)",
            company="Abree Cloud",
            description="طراحی APIهای مقاوم و مدل‌های داده برای یک پلتفرم SaaS.",
            location="دورکاری",
            type="full_time",
            mode="hybrid",
            level="senior",
            salary_range="۵۰,۰۰۰,۰۰۰ - ۷۰,۰۰۰,۰۰۰ تومان",
            skills="Python,FastAPI,PostgreSQL,Docker",
            is_featured=True,
            budget=350000,
        )
        job3 = Job(
            owner_id=dev.id,
            title="ساخت یک صفحه فرود (Landing Page)",
            company="فریلنس",
            description="یک صفحه فرود ایستا برای یک استارتاپ.",
            location="دورکاری",
            type="freelance",
            mode="remote",
            level="junior",
            skills="HTML,CSS,React",
            budget=18000000,
        )
        db.add_all([job1, job2, job3])
        db.flush()

        # Roadmaps
        for key, data in ROADMAPS.items():
            roadmap = Roadmap(
                title=data["title"],
                subtitle=data["subtitle"],
                description=data["description"],
                category=data["category"],
                color=data["color"],
            )
            db.add(roadmap)
            db.flush()
            for stage in data["stages"]:
                db.add(
                    RoadmapStage(
                        roadmap_id=roadmap.id,
                        order=stage["order"],
                        title=stage["title"],
                        description=stage["description"],
                        content=stage["content"],
                        resources=stage["resources"],
                        project=stage["project"],
                        checkpoint=stage["checkpoint"],
                    )
                )

        # Courses
        for key, data in COURSES.items():
            course = Course(
                title=data["title"],
                description=data["description"],
                category=data["category"],
                level=data["level"],
                instructor_name=data["instructor_name"],
                is_free=data["is_free"],
                duration_hours=data["duration_hours"],
            )
            db.add(course)
            db.flush()
            for lesson in data["lessons"]:
                db.add(
                    Lesson(
                        course_id=course.id,
                        order=lesson["order"],
                        title=lesson["title"],
                        content=lesson["content"],
                        video_url=lesson.get("video_url"),
                        duration_minutes=lesson["duration_minutes"],
                    )
                )

        db.add(CourseEnrollment(course_id=1, user_id=dev.id, progress=0.5))

        # Marketplace
        product1 = Product(
            seller_id=dev.id,
            title="قالب داشبورد SaaS فارسی",
            description="یک قالب داشبورد واکنش‌گرا و مدرن ساخته‌شده با React و Tailwind CSS.",
            category="template",
            price=1290000,
            currency="IRR",
            tags="react,typescript,dashboard",
            rating=4.9,
            sales=240,
        )
        product2 = Product(
            seller_id=dev.id,
            title="API آماده تأیید هویت (OTP)",
            description="API تأیید هویت OTP آماده تولید با محدودیت نرخ (rate limiting).",
            category="api",
            price=390000,
            currency="IRR",
            tags="otp,api,verification",
            rating=4.8,
            sales=480,
        )
        product3 = Product(
            seller_id=employer.id,
            title="افزونه رزومه توسعه‌دهنده",
            description="افزونه‌ای که از پروفایل GitHub یک نمونه‌کار توسعه‌دهنده می‌سازد.",
            category="plugin",
            price=790000,
            currency="IRR",
            tags="plugin,resume,portfolio",
            rating=4.7,
            sales=112,
        )
        db.add_all([product1, product2, product3])
        db.flush()
        db.add(Order(product_id=product1.id, buyer_id=employer.id, amount=product1.price, currency="IRR", status="paid"))

        # Payments
        tx = Transaction(
            user_id=dev.id,
            amount=100,
            currency="USD",
            status="succeeded",
            provider="stripe",
            reference="demo_tx_001",
            description="تراکنش نمایشی",
        )
        db.add(tx)
        db.flush()
        db.add(Payment(transaction_id=tx.id, method="card", paid_at=tx.created_at))

        db.commit()
        logger.info("Seeded demo data for DevHub")
    finally:
        db.close()
