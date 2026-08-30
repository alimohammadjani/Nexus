import { useMemo, useState, type CSSProperties } from 'react'
import { Link } from 'react-router-dom'

type Track = {
  id: string
  title: string
  subtitle: string
  color: string
  stages: string[]
  resources: string[]
  project: string
  checkpoint: string
}

type BoardItem = {
  type: 'رایگان' | 'پولی'
  title: string
  stack: string
  level: string
  time: string
  budget: string
}

const tracks: Track[] = [
  {
    id: 'frontend',
    title: 'Frontend Developer',
    subtitle: 'React، UI، performance و تجربه کاربری',
    color: '#7c3aed',
    stages: ['HTML/CSS حرفه‌ای', 'JavaScript عمیق', 'React + TypeScript', 'تست و بهینه‌سازی'],
    resources: ['مینی‌دوره رایگان YouTube', 'مقاله‌های MDN', 'داک رسمی React'],
    project: 'ساخت داشبورد فروش SaaS با نمودار، فیلتر و حالت تاریک',
    checkpoint: 'Code review + تست کامپوننت‌ها + امتیاز UX',
  },
  {
    id: 'backend',
    title: 'Backend Developer',
    subtitle: 'API، دیتابیس، امنیت و معماری سرویس‌ها',
    color: '#0ea5e9',
    stages: ['Python/Node پایه', 'REST API', 'PostgreSQL', 'Auth و Deploy'],
    resources: ['FastAPI Docs', 'PostgreSQL Tutorial', 'Backend Roadmap'],
    project: 'طراحی API مارکت با پرداخت، آپلود فایل و گزارش فروش',
    checkpoint: 'تست endpointها + بررسی امنیت + مستندات OpenAPI',
  },
  {
    id: 'devops',
    title: 'DevOps Engineer',
    subtitle: 'Linux، Docker، CI/CD و مانیتورینگ',
    color: '#10b981',
    stages: ['Linux و شبکه', 'Docker', 'CI/CD', 'Cloud Monitoring'],
    resources: ['Docker Docs', 'GitHub Actions Lab', 'Linux Journey'],
    project: 'دیپلوی یک اپ Full-stack با pipeline خودکار و health check',
    checkpoint: 'بررسی uptime + امنیت secrets + log و alert',
  },
  {
    id: 'mobile',
    title: 'Mobile Developer',
    subtitle: 'React Native، Flutter، API و انتشار اپ',
    color: '#f97316',
    stages: ['UI موبایل', 'State management', 'API integration', 'Release'],
    resources: ['React Native Docs', 'Flutter Codelabs', 'Mobile UX Guide'],
    project: 'اپ مدیریت پروژه فریلنسری با اعلان و پرداخت درون‌برنامه‌ای',
    checkpoint: 'تست روی دستگاه + performance + checklist انتشار',
  },
]

const pillars = [
  { icon: '🗺️', title: 'یادگیری رایگان', description: 'Roadmap تعاملی، منابع رایگان، پروژه عملی، checkpoint و ساخت پورتفولیو خودکار.', metric: '۴ مسیر فعال', to: '/learning' },
  { icon: '💼', title: 'درخواست کار', description: 'پروژه متن‌باز برای تجربه واقعی و پروژه فریلنسری کوتاه‌مدت با بودجه شفاف.', metric: '۱۲۸ فرصت', to: '/jobs' },
  { icon: '🏢', title: 'استخدام نیرو', description: 'آگهی‌های پولی شرکت‌ها با امکان مشاهده پورتفولیوی واقعی و تأیید مهارت.', metric: '۳۶ شرکت', to: '/jobs/new' },
  { icon: '🛒', title: 'مارکت ابزار', description: 'فروش کد، قالب، پلاگین، API و اسکریپت با ریویو، رتبه‌بندی و کمیسیون پلتفرم.', metric: '۲.۱ میلیارد فروش', to: '/market' },
]

const boardItems: BoardItem[] = [
  { type: 'رایگان', title: 'همکاری روی Design System متن‌باز', stack: 'React / Storybook', level: 'جونیور', time: '۶ ساعت/هفته', budget: 'تجربه + Badge' },
  { type: 'پولی', title: 'ساخت صفحه پرداخت برای SaaS', stack: 'Next.js / Stripe', level: 'میدل', time: '۵ روز', budget: '۱۸ میلیون تومان' },
  { type: 'پولی', title: 'API احراز هویت و پنل ادمین', stack: 'FastAPI / PostgreSQL', level: 'سینیور', time: '۱۰ روز', budget: '۳۵ میلیون تومان' },
]

const products = [
  { title: 'قالب داشبورد SaaS فارسی', category: 'Template', price: '۱,۲۹۰,۰۰۰ تومان', rating: '۴.۹', sales: '۲۴۰ فروش' },
  { title: 'API آماده ارسال OTP', category: 'API', price: '۳۹۰,۰۰۰ تومان', rating: '۴.۸', sales: '۴۸۰ فروش' },
  { title: 'پلاگین مدیریت رزومه توسعه‌دهنده', category: 'Plugin', price: '۷۹۰,۰۰۰ تومان', rating: '۴.۷', sales: '۱۱۲ فروش' },
]

const employers = [
  { name: 'نوآوا فین‌تک', role: 'Frontend Mid-level', mode: 'ریموت', match: '۹۴٪' },
  { name: 'ابرینو کلاد', role: 'DevOps Engineer', mode: 'هیبرید', match: '۸۹٪' },
  { name: 'کدآفرین', role: 'Backend FastAPI', mode: 'حضوری', match: '۹۱٪' },
]

export default function Home() {
  const [activeTrackId, setActiveTrackId] = useState(tracks[0].id)
  const activeTrack = useMemo(() => tracks.find((t) => t.id === activeTrackId) ?? tracks[0], [activeTrackId])

  return (
    <div className="app-shell" dir="rtl">
      <section id="hero" className="hero-section section-grid">
        <div className="hero-copy">
          <span className="eyebrow">پلتفرم یکپارچه رشد برنامه‌نویس‌ها</span>
          <h1>یاد بگیر، پورتفولیو بساز، کار پیدا کن و ابزار بفروش.</h1>
          <p className="hero-lead">
            DevHub مسیر کامل «از صفر تا استخدام» را در یک محصول حرفه‌ای جمع کرده؛ آموزش رایگان، پروژه واقعی، فرصت کاری، استخدام نیرو و مارکت ابزار همه به هم وصل‌اند.
          </p>
          <div className="hero-actions">
            <Link className="primary-button" to="/learning">مشاهده Roadmap</Link>
            <Link className="secondary-button" to="/jobs">دیدن فرصت‌ها</Link>
          </div>
          <div className="trust-row" aria-label="آمار DevHub">
            <div><strong>۳۲K+</strong><span>توسعه‌دهنده</span></div>
            <div><strong>۸۵۰+</strong><span>پروژه واقعی</span></div>
            <div><strong>۱۵-۲۰٪</strong><span>کمیسیون مارکت</span></div>
          </div>
        </div>

        <div className="hero-visual" aria-label="نمایش داشبورد DevHub">
          <div className="dashboard-card main-dashboard">
            <div className="window-bar"><span /><span /><span /><strong>DevHub OS</strong></div>
            <div className="profile-strip">
              <div className="avatar">س</div>
              <div><strong>سارا محمدی</strong><span>Frontend Developer • آماده همکاری</span></div>
              <b>۹۲٪ تکمیل</b>
            </div>
            <div className="dashboard-grid">
              <article className="mini-card progress-card">
                <span>Roadmap فعال</span>
                <strong>React + TypeScript</strong>
                <div className="progress-line"><i /></div>
                <small>Checkpoint بعدی: تست کامپوننت</small>
              </article>
              <article className="mini-card"><span>پورتفولیو خودکار</span><strong>۷ پروژه</strong><small>۳ پروژه تأیید مهارت شده</small></article>
              <article className="mini-card income-card"><span>درآمد مارکت</span><strong>۱۴.۸M</strong><small>از فروش قالب و API</small></article>
            </div>
            <div className="stack-list"><span>React</span><span>FastAPI</span><span>Docker</span><span>PostgreSQL</span></div>
          </div>
          <div className="floating-card card-left"><span>Skill Verified</span><strong>UI Engineer</strong></div>
          <div className="floating-card card-right"><span>Match Job</span><strong>۹۴٪</strong></div>
        </div>
      </section>

      <section className="pillars-section" aria-label="چهار بخش اصلی DevHub">
        {pillars.map((pillar) => (
          <Link className="pillar-card" to={pillar.to} key={pillar.title}>
            <div className="pillar-icon">{pillar.icon}</div>
            <span>{pillar.metric}</span>
            <h2>{pillar.title}</h2>
            <p>{pillar.description}</p>
          </Link>
        ))}
      </section>

      <section id="learning" className="content-section learning-section">
        <div className="section-heading">
          <span className="eyebrow">بخش ۱ — یادگیری رایگان</span>
          <h2>Roadmap تعاملی که مستقیم به پورتفولیو وصل می‌شود.</h2>
          <p>کاربر مسیر شغلی خودش را انتخاب می‌کند؛ هر مرحله با منابع رایگان، پروژه عملی و checkpoint سنجش پیشرفت همراه است.</p>
        </div>
        <div className="track-tabs" role="tablist">
          {tracks.map((track) => (
            <button
              className={track.id === activeTrack.id ? 'active' : ''}
              key={track.id}
              onClick={() => setActiveTrackId(track.id)}
              style={{ '--track-color': track.color } as CSSProperties}
              type="button"
            >
              {track.title.replace(' Developer', '')}
            </button>
          ))}
        </div>
        <div className="roadmap-showcase">
          <div className="roadmap-panel" style={{ '--track-color': activeTrack.color } as CSSProperties}>
            <div className="panel-heading"><span>مسیر انتخابی</span><h3>{activeTrack.title}</h3><p>{activeTrack.subtitle}</p></div>
            <ol className="timeline">
              {activeTrack.stages.map((stage, index) => (
                <li key={stage}><span>{index + 1}</span><strong>{stage}</strong></li>
              ))}
            </ol>
          </div>
          <div className="resource-panel">
            <article><span>منابع رایگان</span><ul>{activeTrack.resources.map((r) => <li key={r}>{r}</li>)}</ul></article>
            <article><span>پروژه عملی</span><p>{activeTrack.project}</p></article>
            <article><span>Checkpoint</span><p>{activeTrack.checkpoint}</p></article>
          </div>
        </div>
      </section>

      <section id="work" className="content-section split-section">
        <div className="section-heading align-start">
          <span className="eyebrow">بخش ۲ — درخواست کار</span>
          <h2>از پروژه تمرینی تا درآمد واقعی، با پروفایلی که خودکار پر می‌شود.</h2>
          <p>فرصت‌ها براساس زبان برنامه‌نویسی، سطح و زمان فیلتر می‌شوند؛ پروژه‌های انجام‌شده هم مستقیم وارد پروفایل و پورتفولیو می‌شوند.</p>
          <div className="filter-chips"><span>JavaScript</span><span>Python</span><span>جونیور</span><span>ریموت</span></div>
        </div>
        <div className="job-board">
          {boardItems.map((item) => (
            <article className="job-card" key={item.title}>
              <div><span className={item.type === 'پولی' ? 'paid-badge' : 'free-badge'}>{item.type}</span><h3>{item.title}</h3><p>{item.stack}</p></div>
              <dl><div><dt>سطح</dt><dd>{item.level}</dd></div><div><dt>زمان</dt><dd>{item.time}</dd></div><div><dt>بودجه</dt><dd>{item.budget}</dd></div></dl>
            </article>
          ))}
        </div>
      </section>

      <section id="hiring" className="content-section hiring-section">
        <div className="hiring-card">
          <div className="section-heading align-start">
            <span className="eyebrow">بخش ۳ — استخدام نیرو</span>
            <h2>کارفرما فقط رزومه نمی‌بیند؛ شواهد واقعی مهارت را می‌بیند.</h2>
            <p>شرکت‌ها آگهی پولی ثبت می‌کنند، با فیلتر مهارت، سطح و موقعیت نیرو پیدا می‌کنند و قبل از مصاحبه پروژه‌های تأییدشده کاربر را می‌بینند.</p>
          </div>
          <div className="employer-list">
            {employers.map((employer) => (
              <article key={employer.name}><div><strong>{employer.name}</strong><span>{employer.role}</span></div><small>{employer.mode}</small><b>{employer.match}</b></article>
            ))}
          </div>
        </div>
        <div className="verification-panel">
          <span>سیستم تأیید مهارت</span>
          <h3>Verified by Projects</h3>
          <div className="verify-ring">۸۸٪</div>
          <ul><li>۳ پروژه واقعی بررسی شده</li><li>۲ Code Review موفق</li><li>۱ همکاری تیمی متن‌باز</li></ul>
        </div>
      </section>

      <section id="market" className="content-section market-section">
        <div className="section-heading">
          <span className="eyebrow">بخش ۴ — مارکت ابزار</span>
          <h2>هر توسعه‌دهنده می‌تواند محصول دیجیتال خودش را بفروشد.</h2>
          <p>کد، قالب، پلاگین، اسکریپت و API با سیستم ریویو و رتبه‌بندی منتشر می‌شوند؛ درآمد اصلی پلتفرم از کمیسیون هر فروش است.</p>
        </div>
        <div className="market-grid">
          {products.map((product) => (
            <article className="product-card" key={product.title}>
              <div className="product-preview"><span>{product.category}</span></div>
              <div className="product-body"><h3>{product.title}</h3><div className="rating-row"><span>★ {product.rating}</span><span>{product.sales}</span></div><strong>{product.price}</strong></div>
            </article>
          ))}
        </div>
      </section>

      <section className="content-section advantage-section">
        <div className="section-heading"><span className="eyebrow">چرا منحصربه‌فرده؟</span><h2>DevHub چهار محصول جدا را به یک مسیر درآمدزا تبدیل می‌کند.</h2></div>
        <div className="compare-grid">
          <article><span>LinkedIn</span><p>جاب دارد، اما آموزش و پروژه واقعی ندارد.</p></article>
          <article><span>Udemy</span><p>آموزش دارد، اما مسیر استخدام و مارکت ندارد.</p></article>
          <article><span>Gumroad</span><p>فروش دارد، اما یادگیری و اعتبارسنجی مهارت ندارد.</p></article>
          <article className="highlight-compare"><span>DevHub</span><p>یادگیری، پروژه، استخدام و فروش ابزار را به هم وصل می‌کند.</p></article>
        </div>
      </section>

      <section id="start" className="cta-section">
        <div><span className="eyebrow">مدل درآمدی آماده رشد</span><h2>کمیسیون مارکت، آگهی استخدام پریمیوم و ۱۰٪ کمیسیون پروژه پولی.</h2><p>یک backend کامل و رابط حرفه‌ای برای معرفی محصول، جذب توسعه‌دهنده و متقاعد کردن کارفرماها.</p></div>
        <Link className="primary-button" to="/register">شروع مسیر از امروز</Link>
      </section>
    </div>
  )
}
