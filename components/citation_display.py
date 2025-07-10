import streamlit as st


class CitationDisplay:
    def __init__(self, citation_manager):
        self.citation_manager = citation_manager

    def render(self):
        """Render the citation display interface"""
        st.subheader("📚 Citation Library")

        with st.expander("➕ Add New Citation"):
            self._render_add_citation()

        self._render_search_filter()

        self._render_citations_list()

        self._render_export_options()

    def _render_add_citation(self):
        """Render add citation form"""
        with st.form("add_citation"):
            col1, col2 = st.columns(2)

            with col1:
                title = st.text_input("Title *", placeholder="Paper title")
                authors = st.text_area("Authors", placeholder="Author1, Author2, Author3")
                year = st.number_input("Year", min_value=1900, max_value=2030, value=2024)
                journal = st.text_input("Journal/Conference", placeholder="Journal name")

            with col2:
                volume = st.text_input("Volume", placeholder="Volume number")
                pages = st.text_input("Pages", placeholder="1-10")
                doi = st.text_input("DOI", placeholder="10.1000/182")
                url = st.text_input("URL", placeholder="https://...")

            abstract = st.text_area("Abstract", placeholder="Paper abstract...")
            keywords = st.text_input("Keywords", placeholder="keyword1, keyword2, keyword3")
            notes = st.text_area("Notes", placeholder="Personal notes about this paper...")

            if st.form_submit_button("Add Citation"):
                if title:
                    authors_list = [a.strip() for a in authors.split(',')] if authors else []
                    keywords_list = [k.strip() for k in keywords.split(',')] if keywords else []

                    citation_data = {
                        'title': title,
                        'authors': authors_list,
                        'year': year,
                        'journal': journal,
                        'volume': volume,
                        'pages': pages,
                        'doi': doi,
                        'url': url,
                        'abstract': abstract,
                        'keywords': keywords_list,
                        'notes': notes
                    }

                    citation_id = self.citation_manager.add_citation(citation_data)
                    st.success(f"Citation added successfully! ID: {citation_id}")
                    st.rerun()
                else:
                    st.error("Please provide at least a title")

    def _render_search_filter(self):
        """Render search and filter options"""
        col1, col2, col3 = st.columns(3)

        with col1:
            search_query = st.text_input("🔍 Search citations", placeholder="Search by title, author, or keyword...")

        with col2:
            year_range = st.slider("Year range", min_value=1900, max_value=2030, value=(2000, 2024))

        with col3:
            sort_by = st.selectbox("Sort by", ["Date Added", "Title", "Year", "Authors"])

        st.session_state.search_query = search_query
        st.session_state.year_range = year_range
        st.session_state.sort_by = sort_by

    def _render_citations_list(self):
        """Render list of citations"""
        citations = self.citation_manager.get_all_citations()

        if not citations:
            st.info("No citations added yet. Click 'Add New Citation' to get started.")
            return

        filtered_citations = self._filter_citations(citations)

        if not filtered_citations:
            st.info("No citations match your search criteria.")
            return

        for citation in filtered_citations:
            self._render_citation_card(citation)

    def _filter_citations(self, citations):
        """Filter citations based on search and filter criteria"""
        filtered = citations.copy()

        if hasattr(st.session_state, 'search_query') and st.session_state.search_query:
            query = st.session_state.search_query.lower()
            filtered = [c for c in filtered if
                        query in c['title'].lower() or
                        any(query in author.lower() for author in c['authors']) or
                        any(query in keyword.lower() for keyword in c['keywords'])]

        if hasattr(st.session_state, 'year_range'):
            min_year, max_year = st.session_state.year_range
            filtered = [c for c in filtered if min_year <= c['year'] <= max_year]

        if hasattr(st.session_state, 'sort_by'):
            if st.session_state.sort_by == "Date Added":
                filtered.sort(key=lambda x: x['added_at'], reverse=True)
            elif st.session_state.sort_by == "Title":
                filtered.sort(key=lambda x: x['title'])
            elif st.session_state.sort_by == "Year":
                filtered.sort(key=lambda x: x['year'], reverse=True)
            elif st.session_state.sort_by == "Authors":
                filtered.sort(key=lambda x: x['authors'][0] if x['authors'] else "")

        return filtered

    def _render_citation_card(self, citation):
        """Render individual citation card"""
        with st.expander(f"📄 {citation['title']} ({citation['year']})"):
            col1, col2 = st.columns([2, 1])

            with col1:
                st.write(f"**Authors:** {', '.join(citation['authors'])}")
                st.write(f"**Year:** {citation['year']}")
                if citation['journal']:
                    st.write(f"**Journal:** {citation['journal']}")
                if citation['doi']:
                    st.write(f"**DOI:** {citation['doi']}")
                if citation['url']:
                    st.write(f"**URL:** {citation['url']}")

                if citation['abstract']:
                    st.write("**Abstract:**")
                    st.write(citation['abstract'])

                if citation['keywords']:
                    st.write(f"**Keywords:** {', '.join(citation['keywords'])}")

                if citation['notes']:
                    st.write("**Notes:**")
                    st.write(citation['notes'])

            with col2:
                st.write("**Citation Formats:**")

                apa_citation = self.citation_manager.format_citation(citation['id'], "apa")
                st.text_area("APA", apa_citation, height=100, key=f"apa_{citation['id']}")

                mla_citation = self.citation_manager.format_citation(citation['id'], "mla")
                st.text_area("MLA", mla_citation, height=100, key=f"mla_{citation['id']}")

                col_edit, col_delete = st.columns(2)

                with col_edit:
                    if st.button("✏️ Edit", key=f"edit_{citation['id']}"):
                        st.info("Edit functionality coming soon!")

                with col_delete:
                    if st.button("🗑️ Delete", key=f"delete_{citation['id']}"):
                        if self.citation_manager.delete_citation(citation['id']):
                            st.success("Citation deleted successfully!")
                            st.rerun()
                        else:
                            st.error("Failed to delete citation")

    def _render_export_options(self):
        """Render export options for citations"""
        st.subheader("📤 Export Citations")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Export as BibTeX"):
                bibtex_data = self.citation_manager.export_citations("bibtex")
                if bibtex_data:
                    st.download_button(
                        label="Download BibTeX",
                        data=bibtex_data,
                        file_name="citations.bib",
                        mime="text/plain"
                    )
                else:
                    st.info("No citations to export")

        with col2:
            if st.button("Export as CSV"):
                csv_data = self.citation_manager.export_citations("csv")
                if csv_data:
                    st.download_button(
                        label="Download CSV",
                        data=csv_data,
                        file_name="citations.csv",
                        mime="text/csv"
                    )
                else:
                    st.info("No citations to export")
