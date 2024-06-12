# lib/bulma_pagination_renderer.rb
require 'will_paginate/view_helpers/action_view'
class BulmaPaginationRenderer < WillPaginate::ActionView::LinkRenderer
  def container_attributes
    { class: 'pagination is-centered', role: 'navigation', 'aria-label': 'pagination' }
  end

  def previous_or_next_page(page, text, classname)
    classnames = ['pagination-link']
    classnames << (page ? '' : 'is-disabled')
    classnames << classname

    if classname == 'previous_page'
      link(text, page || '#', class: classnames.join(' '))
    elsif classname == 'next_page'
      link(text, page || '#', class: classnames.join(' '))
    end
  end

  def page_number(page)
    classnames = ['pagination-link']
    classnames << 'is-current' if page == current_page

    tag(:a, page, class: classnames.join(' '), href: page == current_page ? nil : url(page), 'aria-label': "Goto page #{page}")
  end

  def gap
    tag(:span, '&hellip;', class: 'pagination-ellipsis')
  end

  def html_container(html)
    tag(:nav, tag(:ul, html, class: 'pagination-list'), container_attributes)
  end
end