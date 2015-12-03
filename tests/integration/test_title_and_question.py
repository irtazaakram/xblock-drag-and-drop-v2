from ddt import ddt, unpack, data
from selenium.common.exceptions import NoSuchElementException
from tests.integration.test_base import BaseIntegrationTest
from workbench import scenarios


@ddt
class TestDragAndDropTitleAndQuestion(BaseIntegrationTest):
    @unpack
    @data(
        ('plain1', 'title1', 'question1'),
        ('plain2', 'title2', 'question2'),
        ('html1', 'title with <i>HTML</i>', 'Question with <i>HTML</i>'),
        ('html2', '<span style="color:red">Title: HTML?</span>', '<span style="color:red">Span question</span>'),
    )
    def test_title_and_question_parameters(self, _, display_name, question_text):
        const_page_name = 'Test title and question parameters'
        const_page_id = 'test_block_title_and_question'
        scenario_xml = self._make_scenario_xml(
            display_name=display_name, show_title=True, question_text=question_text, completed=False
        )
        scenarios.add_xml_scenario(const_page_id, const_page_name, scenario_xml)
        self.addCleanup(scenarios.remove_scenario, const_page_id)

        page = self.go_to_page(const_page_name)
        problem_header = page.find_element_by_css_selector('h2.problem-header')
        self.assertEqual(self.get_element_html(problem_header), display_name)

        question = page.find_element_by_css_selector('section.problem > p')
        self.assertEqual(self.get_element_html(question), question_text)

    @unpack
    @data(
        ('plain shown', 'title1', True),
        ('plain hidden', 'title2', False),
        ('html shown', 'title with <i>HTML</i>', True),
        ('html hidden', '<span style="color:red">Title: HTML?</span>', False)
    )
    def test_show_title_parameter(self, _, display_name, show_title):
        const_page_name = 'Test show title parameter'
        const_page_id = 'test_block_show_title'
        scenario_xml = self._make_scenario_xml(
            display_name=display_name, show_title=show_title, question_text='Generic question', completed=False
        )
        scenarios.add_xml_scenario(const_page_id, const_page_name, scenario_xml)
        self.addCleanup(scenarios.remove_scenario, const_page_id)

        page = self.go_to_page(const_page_name)
        if show_title:
            problem_header = page.find_element_by_css_selector('h2.problem-header')
            self.assertEqual(self.get_element_html(problem_header), display_name)
        else:
            with self.assertRaises(NoSuchElementException):
                page.find_element_by_css_selector('h2.problem-header')