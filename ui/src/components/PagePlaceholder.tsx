interface Props {
  title: string
}

export default function PagePlaceholder({ title }: Props) {
  return (
    <section>
      <h1>{title}</h1>
      <p>Geliştirme aşamasında</p>
    </section>
  )
}
