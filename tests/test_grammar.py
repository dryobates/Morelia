from unittest import TestCase

from mock import sentinel, Mock, ANY

from morelia.decorators import tags
from morelia.formatters import IFormatter
from morelia.grammar import Feature, Node, Step, SourceLocation, Tag
from morelia.matchers import IStepMatcher
from morelia.parser import AST
from morelia.visitors import IVisitor


@tags(['unit'])
class ASTEvaluateTestCase(TestCase):
    """ Test :py:meth:`AST.evaluate`. """

    def test_should_use_provided_matcher(self):
        """ Scenariusz: matcher given as parameter """
        # Arrange
        test_visitor_class = Mock(IVisitor)
        matcher_class = Mock(IStepMatcher)
        feature = Mock(Feature)
        steps = [feature]
        obj = AST(steps, test_visitor_class=test_visitor_class)
        # Act
        obj.evaluate(sentinel.suite, matchers=[matcher_class])
        # Assert
        test_visitor_class.assert_called_once_with(sentinel.suite, matcher_class.return_value, ANY, ANY)

    def test_should_use_provided_formatter(self):
        """ Scenariusz: formatter given as parameter """
        # Arrange
        test_visitor = Mock(IVisitor)
        formatter = Mock(IFormatter)
        feature = Mock(Feature)
        steps = [feature]
        obj = AST(steps, test_visitor_class=test_visitor)
        # Act
        obj.evaluate(sentinel.suite, formatter=formatter)
        # Assert
        test_visitor.assert_called_once_with(sentinel.suite, ANY, formatter, ANY)

    def test_should_show_all_missing_steps(self):
        """ Scenariusz: show all missing steps """
        # Arrange
        matcher_visitor = Mock(IVisitor)
        feature = Mock(Feature)
        steps = [feature]
        obj = AST(steps, matcher_visitor_class=matcher_visitor)
        suite = Mock()
        # Act
        obj.evaluate(suite, show_all_missing=True)
        # Assert
        matcher_visitor.assert_called_once_with(suite, ANY)


@tags(['unit'])
class LabeledNodeGetLabelsTestCase(TestCase):

    def test_should_return_node_labels(self):
        """ Scenario: node labels """
        # Arrange
        expected = ['label1', 'label2']
        obj = Feature(None, None, labels=expected)
        # Act
        result = obj.get_labels()
        # Assert
        self.assertEqual(result, expected)

    def test_should_return_node_and_parent_labels(self):
        """ Scenario: node and parent labels """
        # Arrange
        expected = ['label1', 'label2']
        obj = Feature(None, None, labels=['label1'])
        parent = Feature(None, None, labels=['label2'])
        obj.parent = parent
        # Act
        result = obj.get_labels()
        # Assert
        self.assertEqual(result, expected)


@tags(['unit'])
class INodeEvaluateStepsTest(TestCase):

    node_class = Node

    def test_should_call_visitor(self):
        # Arrange
        node = self.node_class('Feature', 'Some feature')
        visitor = Mock(IVisitor)
        # Act
        node.accept(visitor)
        # Assert
        visitor.visit.assert_called_once_with(node)

    def test_should_evaluate_child_steps(self):
        # Arrange
        steps = [Mock(Step), Mock(Step)]
        node = self.node_class('Feature', 'Some feature', steps=steps)
        visitor = Mock(IVisitor)
        # Act
        node.accept(visitor)
        # Assert
        visitor.visit.assert_called_once_with(node)
        for step in steps:
            step.accept.assert_called_once_with(visitor)


@tags(['unit'])
class FeatureTest(TestCase):

    def test_returns_default_uri(self):
        keyword = 'Feature'
        predicate = 'Feature with scenario'
        feature = Feature(keyword, predicate)
        self.assertEqual('<string>', feature.uri)

    def test_returns_filename_uri(self):
        keyword = 'Feature'
        predicate = 'Feature with scenario'
        feature = Feature(keyword, predicate, source=SourceLocation(sentinel.filename, sentinel.line))
        self.assertEqual(sentinel.filename, feature.uri)

    def test_returns_node_info(self):
        keyword = 'Feature'
        predicate = 'Feature with scenario\nDescription of a feature'
        feature = Feature(keyword, predicate, source=SourceLocation(sentinel.filename, sentinel.line))
        info = feature.get_info()
        self.assertEqual(sentinel.filename, info['uri'])
        self.assertEqual('Feature', info['keyword'])
        self.assertEqual('feature-with-scenario', info['id'])
        self.assertEqual('Feature with scenario', info['name'])
        self.assertEqual(sentinel.line, info['line'])
        self.assertEqual('Description of a feature', info['description'])

    def test_returns_tags_in_info_dict(self):
        keyword = 'Feature'
        predicate = 'Feature with scenario'
        tags = [Tag('tag1', 1), Tag('tag2', 1)]
        feature = Feature(keyword, predicate, tags=tags)
        info = feature.get_info()
        tags = info['tags']
        self.assertEqual(tags, info['tags'])
